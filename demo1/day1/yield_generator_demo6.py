# -*- coding: utf-8
def my_generator():
    print("return first value")
    yield 1
    print("return second value")
    yield 2
    print("return last value")
    yield 3
    print("raise StopIteration")

z = my_generator()
next(z)
next(z)
next(z)
# next(z)
print('-'*50)
def foo():
    print('\tbegin\t')
    for i in range(3):
        print('before generate ',i)
        yield i
        print('after generate ', i)
    print('\tend\t')

f=foo()
next(f)
next(f)
next(f)

print '我爱我家'