import functools
import time


@functools.lru_cache()
def add(x, y, z=3):
    time.sleep(z)
    return x + y


print(add(4, 5))
print(add(4.0, 5))
print(add(4, 6))
print(add(4, 6, 3))
print(add(3, 2))
print(add(2, y=3))
print(add(x=40, y=60))
print(add(y=60, x=40))
