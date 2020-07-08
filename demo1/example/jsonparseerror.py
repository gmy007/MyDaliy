#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jsonparseerror.py -- json解析过程相关异常类
"""


class JsonParseError(Exception):
    u"""jsonparser模块所有异常对象的基类"""
    pass


class JsonFormatError(JsonParseError):
    u"""json格式错误相关异常"""
    pass
