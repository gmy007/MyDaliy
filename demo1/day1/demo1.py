    # -*- coding: utf-8
print('{:_^13}'.format('hello'))

'''
Numbers 
String
List    列表  []
      Method:list.sort()
             list.append()
             len(list)
            
Tuple   元组  ()  不可变

Dictionary  字典  {}
    key: value
    key不可变 value可变

Set:    集合
'''

str1 = 'hello world!'
str2 = str1[0:2]

print str1, str2

list1 = [str2, str1, [str2, str1, str2[0]]]
print(list1, list1[0:1])

list2 = list()
print(list2.append(list1[0]), list2)

print()
dic1 = {'Swaroop': 'swaroop@swaroopch.com',
        'Larry': 'larry@wall.org',
        'Matsumoto': 'matz@ruby-lang.org',
        'Spammer': 'spammer@hotmail.com'}

print(dic1.items())
print(dic1.keys())
print(dic1.values())

'''
列表、元组、字符串可以看作‘序列’
序列的主要功能为资格测试：in/not in 和索引操作
'''
print()
if 'Larry' in dic1:
    print(dic1['Larry'])
else:
    print("Larry not in dict1")

shoplist = ['apple', 'banana', 'carrot', 'mango']
# 切片
print(shoplist[-1])
print(shoplist[::2])
print(shoplist[1:-1])
print(shoplist[::-1])

'''
函数：
    def funcName(a,b,c)
    默认参数 def funName(a=1)
    可变参数 def funName(*a,**b) 
        一个*代表元组，两个*代表字典
'''


def fun1(a=1, *b, **c):
    '''这是一个说明性doc。

    :param a:参数a，默认为1
    :param b:可变参b,元组
    :param c:可变参c，字典
    :return: null
    '''
    print('*' * 10 + 'start' + '*' * 10)
    print('参数a:\t', a)
    print('元组b:\t', b[:-1])
    print('字典c:\t', c.items())
    if 'gmy' in c and 'ljr' in c:
        print('all in c')
        print('*' * 10 + 'end' + '*' * 10)


a = 10
print(fun1.__doc__)
fun1(10, 'abc', 'zxc', [1, 2, 3], gmy=25, ljr=24)

# 判断调用和被调用模块的关系 
if __name__ == '__main__':
    print("This is main start!")
