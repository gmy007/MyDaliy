#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
jsontranslator.py -- 提供让Json字符串和Python中dict、list对象互相转换的方法
1. json_to_object(json_str)：传入json字符串转为Python对象；
2. object_to_json(obj)：传入Python对象（dict、list、tuple）转为对应json字符串
"""

import logging
import string

from jsonparseerror import JsonFormatError
from stringreader import StringReader


log = logging.getLogger()
hexdigits = string.hexdigits


def _process_escape_char(reader, next_ch):
    u"""用于处理，并返回一个合法转义字符"""
    if next_ch == '"':
        escape_char = '"'
    elif next_ch == '\'':
        escape_char = '\''
    elif next_ch == 'n':
        escape_char = '\n'
    elif next_ch == 't':
        escape_char = '\t'
    elif next_ch == 'r':
        escape_char = '\r'
    elif next_ch == 'b':
        escape_char = '\b'
    elif next_ch == 'f':
        escape_char = '\f'
    elif next_ch == '\\':
        escape_char = '\\'
    elif next_ch == 'u':
        # 处理Unicode编码
        unicode_char = '\u'
        for i in range(4):
            ch = reader.get_next()
            if ch not in hexdigits:
                raise JsonFormatError("Invalid hex char : %s" % ch)
            unicode_char += ch
        escape_char = unicode_char.decode("raw_unicode_escape")
    else:
        raise JsonFormatError("Invalid escape char : %s" % next_ch)
    return escape_char


def read_string(reader):
    str_body = ""
    while reader.has_next():
        ch = reader.get_next()

        if ch == '\\':
            # 处理转义字符
            next_ch = reader.get_next()
            escape_char = _process_escape_char(reader, next_ch)
            str_body += escape_char
        elif ch == '"':
            return str_body
        else:
            str_body += ch


def read_number(reader, ch):
    u"""用于读取数字内容，ch表示上一个被读取到的字符"""
    num_str = ch
    isfloat = False
    while reader.has_next():
        ch = reader.get_next()

        if ch.isspace():
            break
        # 读取到逗号,冒号或结束符('}', ']')需要回退一个位置,交给后面的方法处理
        elif ch in (',', ':', '}', ']'):
            reader.get_prev()
            break
        elif ch in ('e', '.'):
            isfloat = True
            num_str += ch
        elif ch.isdigit() or ch == '-':
            num_str += ch
        else:
            raise JsonFormatError("Invalid char when read number : %s" % ch)

    # 根据标记位进行对应转换
    try:
        if isfloat:
            return float(num_str)
        else:
            return int(num_str)
    except ValueError:
        log.warning("Json num format error, string:%s", string)
        raise JsonFormatError("Invalid num format, num string:%s" % string)


def read_non_space_char(reader):
    u"""用于读取下一个非空白字符"""
    while reader.has_next():
        ch = reader.get_next()
        if ch is not None and ch.isspace():
            continue
        return ch
    else:
        return None


def read_identifier(reader, identifier_chars, ret_val):
    u"""
    读取Json中的标识符，比如：null，则传入：('u', 'l', 'l'), None
    头一个字符可以忽略，因为头个字符在判断时已经被读取
    :param reader:
    :param identifier_chars:
    :param ret_val:
    :return:
    """
    length = len(identifier_chars)
    for i in range(length):
        ch = reader.get_next()
        if ch is None or ch != identifier_chars[i]:
            raise JsonFormatError("Invalid identifier value when read %s"
                                  % str(ret_val))
    else:
        return ret_val


def read_null(reader):
    # Null
    return read_identifier(reader, ('u', 'l', 'l'), None)


def read_true(reader):
    # True
    return read_identifier(reader, ('r', 'u', 'e'), True)


def read_false(reader):
    # False
    return read_identifier(reader, ('a', 'l', 's', 'e'), False)


def read_inf(reader):
    # inf
    return read_identifier(reader, ('n', 'f'), float('inf'))


def read_key(reader, ch):
    if ch == '"':
        return read_string(reader)
    else:
        log.warning("Key must be string type")
        raise JsonFormatError("Invalid key type")


def read_value(reader):
    while reader.has_next():
        ch = reader.get_next()
        if ch.isspace():
            continue
        elif ch == '"':
            return read_string(reader)
        elif ch == '-' or ch.isdigit():
            return read_number(reader, ch)
        elif ch in ('i',):
            return read_inf(reader)
        elif ch in ('n',):
            return read_null(reader)
        elif ch in ('t',):
            return read_true(reader)
        elif ch in ('f',):
            return read_false(reader)
        elif ch == '{':
            return read_object(reader)
        elif ch == '[':
            return read_array(reader)
        else:
            raise JsonFormatError("Invalid value format, read char:%s" % ch)


def read_array(reader):
    json_array = []
    while reader.has_next():
        ch = reader.get_next()
        if ch.isspace():
            continue
        if ch == ']':
            break

        # 前移一位，在read_value中获取值
        reader.get_prev()
        json_array.append(read_value(reader))

        # 读取下一个非空字符，判断是否 , 或者 ]
        non_space_char = read_non_space_char(reader)
        if non_space_char == ']':
            break
        elif non_space_char == ',':
            continue
        else:
            log.warning("Char after array value must be ',' or ']', ch:%s", ch)
            raise JsonFormatError(
                "Next char after array value must be ',' or ']', ch:%s" % ch)
    else:
        log.warning("Invalid json array format, lost ']'")
        raise JsonFormatError("Json array lost ']'")
    return json_array


def read_object(reader):
    json_obj = {}
    while reader.has_next():
        ch = reader.get_next()
        if ch.isspace():
            continue
        elif ch == '}':
            break

        # 按照 key , : , value顺序读取数据
        key = read_key(reader, ch)
        ch = read_non_space_char(reader)
        if ch != ":":
            raise JsonFormatError("After key must be colon ':'")
        value = read_value(reader)

        # 忽略非字符串类型的key
        if not isinstance(key, (str, unicode)):
            log.info("Key must be str, key:%s, ignore it.", key)
        else:
            json_obj[key] = value

        # 读取下一个非空字符，判断是否 , 或者 }
        non_space_char = read_non_space_char(reader)
        if non_space_char == '}':
            break
        elif non_space_char == ',':
            continue
        else:
            log.warning("Char after value must be ',' or '}'")
            raise JsonFormatError(
                "Char after value must be ',' or '}', ch:%s" % ch)
    else:
        log.warning("Invalid json obj format, lost '}'")
        raise JsonFormatError("Json obj lost '}'")
    return json_obj


def json_to_object(json):
    if not isinstance(json, (str, unicode)):
        log.debug("Argument type was not str, argument:%s", json)
        raise TypeError("Argument must be str type")

    json = json.strip()
    res_obj = None
    reader = StringReader(json)
    while reader.has_next():
        ch = reader.get_next()
        if ch == '{':
            res_obj = read_object(reader)
        elif ch == '[':
            res_obj = read_array(reader)
        else:
            log.debug("Invalid json format, json string should start with "
                      "start with '{' or '[', argument:%s", json)
            raise JsonFormatError("Json string must start with '{' or '['")
    return res_obj


def _process_string_escape_char(value):
    # 针对 value 中的特殊字符进行处理
    process_value = ""
    for ch in value:
        if ch == '"':
            process_value += "\\\""
        elif ch == '\'':
            process_value += "\\\'"
        elif ch == '\\':
            process_value += "\\\\"
        elif ch == '\n':
            process_value += "\\n"
        elif ch == '\t':
            process_value += "\\t"
        elif ch == '\r':
            process_value += "\\r"
        else:
            process_value += ch
    return process_value


def obj_to_json(obj):
    json = ""
    for key, value in obj.items():
        # 只将key为str类型转换为json
        if not isinstance(key, (str, unicode)):
            log.info("Key was not string type, type:%s, ignore it.", type(key))
            continue

        if isinstance(value, (str, unicode)):
            process_value = _process_string_escape_char(value)
            value_str = "\"%s\"" % process_value
        elif value is True or value is False:
            value_str = "true" if value else "false"
        # 不能使用 isinstance(obj, bool)，因为bool类型也是int类型，会被拦截
        elif isinstance(value, (int, float)):
            value_str = str(value)
        elif isinstance(value, dict):
            value_str = obj_to_json(value)
        elif isinstance(value, (list, tuple)):
            value_str = array_to_json(value)
        elif value is None:
            value_str = "null"
        else:
            log.info("Value was not support type, type:%s", type(value))
            continue
        process_key = _process_string_escape_char(key)
        json += "\"%s\":%s, " % (process_key, value_str)
    return "{%s}" % (json[:-2] if json else "")


def array_to_json(array):
    json = ""
    for item in array:
        if isinstance(item, (str, unicode)):
            item_str = "\"%s\"" % item
        elif isinstance(item, (int, float)):
            item_str = str(item)
        elif isinstance(item, bool):
            item_str = "true" if item else "false"
        elif isinstance(item, dict):
            item_str = obj_to_json(item)
        elif isinstance(item, (list, tuple)):
            item_str = array_to_json(item)
        elif item is None:
            item_str = "null"
        else:
            log.info("Value was not support type, type:%s", type(item))
            continue
        json += "%s, " % item_str
    return "[%s]" % (json[:-2] if json else "")


def object_to_json(obj):
    if isinstance(obj, dict):
        return obj_to_json(obj)
    elif isinstance(obj, (list, tuple)):
        return array_to_json(obj)
    else:
        raise TypeError("Object must be dict, list or tuple type.")


def test():
    json_1 = '{ "id" : 123, "name" : "vison", 123:"invalid", ' \
             '"item" : [True, False, Null]}'
    obj_1 = {"id": 123, "name": "vison", "item": [True, False, None]}
    json_2 = '[{"id": 123, "age": 222}, {"name": "vison", "male": true}, ' \
             '{"name": "minmin", "male": false, 123: "Invalid", "info" : null}]'
    obj_2 = [{"id": 123, "age": 222}, {"name": "vison", "male": True},
             {"name": "minmin", "male": False, "info": None}]

    assert json_to_object(json_1) == obj_1
    assert json_to_object(json_2) == obj_2
    assert object_to_json({}) == '{}'
    assert object_to_json([]) == '[]'


if __name__ == '__main__':
    test()
