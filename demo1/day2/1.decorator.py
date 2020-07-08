# -*- coding: utf-8 -*-
import time, functools


def metric(fn):
    start_time = time.time()

    @functools.wraps(fn)
    def wrapper(*args, **kw):
        result=fn(*args,**kw)
        end_time=time.time()
        print('%s executed in %s ms' % (fn.__name__, end_time-start_time))
        return result
    return wrapper



