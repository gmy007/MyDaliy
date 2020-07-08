# -*- coding: utf-8
# from pprint import pprint
import sys,pprint,demo1
print('命令行参数如下')
for i in sys.argv:
    print(i)

print()
print('Python路径为：\t',sys.path)
data = ("test", [1, 2, 3,'test', 4, 5], "This is a string!",
        {'age':23, 'gender':'F'})
pprint.pprint(data)

pprint.pprint(sys.path)

demo1.fun1(1,data,data)
print(dir(demo1))