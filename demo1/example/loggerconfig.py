#!/usr/bin/env python
# -*- coding: utf-8

"""
loggerconfig.py -- 使用代码配置root logger
"""

import sys
import logging


# 配置root logger，指定格式，使用控制台输出信息
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(console_handler)

# 指定输出级别：DEBUG
logger.setLevel(logging.DEBUG)


logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s: %(message)s')