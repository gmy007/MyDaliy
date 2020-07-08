#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
fileutil.py -- 提供文件读取写入相关方法
"""

import codecs


def read_file(path, encoding="utf-8"):
    u"""
    根据编码和文件路径读取文件内容
    :param path:
    :param encoding:
    :return:
    """
    with codecs.open(path, 'r', encoding=encoding) as fobj:
        content = ""
        for line in fobj:
            content += line.strip()
    return content


def write_file(path, content, mode='w', encoding="utf-8"):
    u"""
    根据编码和指定模式，将内容写入指定文件中
    :param path:
    :param content:
    :param mode:
    :param encoding:
    :return:
    """
    with codecs.open(path, mode, encoding=encoding) as fobj:
        fobj.write(content)
