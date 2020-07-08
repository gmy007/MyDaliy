# -*- coding: utf-8

seasons = ['Spring', 'Summer', 'Fall', 'Winter']

print list(enumerate(seasons))

fun = 'pow(2,3)'
# eval 执行字符串表达式
print  eval(fun)

file = open('d://123.txt', "a+")

print file.readline()
file.close()


def triangles():
    list1 = [1]
    while 1:
        list2 = [1]
        yield list1
        for i in range(len(list1) - 1):
            list2.append(list1[i] + list1[i + 1])
        list2.append(1)
        list1 = list2


def is_odd(n):
    return n % 2 == 1

newlist = filter(is_odd, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print newlist
