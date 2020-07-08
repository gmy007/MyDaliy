#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
stringreader.py -- 用于读取字符串的对象
"""


class StringReader(object):

    def __init__(self, data):
        if not isinstance(data, (str, unicode)):
            raise TypeError("Unsupported type, argument must be str "
                            "or unicode type")
        self._data = data
        self._idx = 0
        self._length = len(data)
        self.ch = ''

    def has_next(self):
        return self._idx < self._length

    def get_next(self):
        if self._idx >= self._length:
            return None
        ch = self._data[self._idx]
        self._idx += 1
        self.ch = ch
        return ch

    def has_prev(self):
        return self._idx > 0

    def get_prev(self):
        if self._idx <= 0:
            return None
        self._idx -= 1
        self.ch=self._data[self._idx]
        return self._data[self._idx]


def test():
    a = StringReader("abcdefgh")
    while a.has_next():
        print a.get_next(),
    print ''

    while a.has_prev():
        print a.get_prev()


if __name__ == '__main__':
    test()
