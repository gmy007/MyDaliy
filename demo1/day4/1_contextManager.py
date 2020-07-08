# coding:utf-8
from contextlib import contextmanager


class Query(object):
    def __init__(self, name):
        self.name = name

    def query(self):
        print 'query info about %s' % self.name


@contextmanager
def create_query(name):
    print 'begin'.center(40, '-')
    q = Query(name)
    yield q
    print 'end'.center(40, '-')


with create_query('gmy') as q:
    q.query()

# 利用contextmanager 和with  前后代理
@contextmanager
def tag(name):
    print '<%s>' % name
    yield   # 方法在yield语句前后执行
    print '<%s>' % name


with tag('h1'):
    print 'hello world'