#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jsonparser.py -- 提供JsonParser类进行json操作，主要提供如下功能：
1. 支持类似Dict操作，如：parser["name"] = "vison"，会更新内部数据；
2. loads(json_str)：支持读取json字符串，生成内部结构；
3. dumps()：支持将内部结构转换成json字符串输出，会自动忽略key为数字的键；
4. update(dict)：支持直接传入一个dict类型的参数，直接更新JsonParser实例的内部结构；
5. load_dict(dict)：同update方法；
6. dump_dict()：建立一个与data一样结构的字典返回；
7. load_file(filepath)：支持从文件中读取json字符串进行解析；
8. dump_file(filepath)：将内部结构转换为json串输出到指定的文件中；
"""

import logging

import fileutil
import jsontranslator

from jsonparseerror import JsonParseError
from jsonparseerror import JsonFormatError


log = logging.getLogger()


class JsonParser(object):

    def __init__(self):
        self._data = {}

    def __setitem__(self, key, value):
        self._check_type()
        self._data[key] = value

    def __getitem__(self, item):
        self._check_type()
        return self._data[item]

    def __delitem__(self, key):
        self._check_type()
        del self._data[key]

    def __contains__(self, item):
        self._check_type()
        return item in self._data

    def _check_type(self):
        if not isinstance(self._data, dict):
            log.warning("Data type was not dict, type:%s", type(self._data))
            raise TypeError("Data type was not dict")

    def loads(self, json_str):
        try:
            json_obj = jsontranslator.json_to_object(json_str)
        except JsonFormatError:
            log.exception("Json format error")
            raise JsonParseError("Json parser error")
        self._data = json_obj

    def dumps(self):
        if isinstance(self._data, dict):
            return jsontranslator.object_to_json(self._data)
        raise JsonParseError("Data type was error, type:%s", type(self._data))

    def update(self, d):
        if not isinstance(d, dict):
            raise TypeError("Argument type must be dict, type:%s", type(d))
        json_str = jsontranslator.object_to_json(d)
        json_obj = jsontranslator.json_to_object(json_str)
        self._data = json_obj

    def load_dict(self, d):
        self.update(d)

    def dump_dict(self):
        self._check_type()
        json_str = jsontranslator.object_to_json(self._data)
        return jsontranslator.json_to_object(json_str)

    def load_file(self, path):
        json_str = fileutil.read_file(path)
        if json_str is not None and json_str:
            json_obj = jsontranslator.json_to_object(json_str)
        else:
            raise JsonParseError("File content was empty .")
        self._data = json_obj

    def dump_file(self, path):
        if self._data is not None:
            json_str = jsontranslator.object_to_json(self._data)
            fileutil.write_file(path, json_str)
