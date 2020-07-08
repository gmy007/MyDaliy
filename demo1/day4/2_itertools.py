# -*- coding: utf-8 -*-
import itertools
import jsonparser, json


def pi(N):
    ' 计算pi的值 '
    # step 1: 创建一个奇数序列: 1, 3, 5, 7, 9, ...
    natures = itertools.count(1, 2)
    # step 2: 取该序列的前N项: 1, 3, 5, 7, 9, ..., 2*N-1.
    siglens = itertools.takewhile(lambda x: x <= 2 * N - 1, natures)
    ret = 0
    status = 1
    for i in siglens:
        ret += status * 4 / i
        status *= -1

    # step 3: 添加正负符号并用4除: 4/1, -4/3, 4/5, -4/7, 4/9, ...

    # step 4: 求和:
    return ret


def fun():
    # enumerate适合用来遍历不带索引的数据，为每个数据提供索引
    print list(enumerate('abcdefghijklmn'))
    for i, data in enumerate('abcdefghijklmn'):
        print i, data


def fun1():
    names = ['cartlina', 'BOB', 'TOM', 'NIKE']
    length = [len(i) for i in names]
    max = 0
    '''
    py2中，zip函数会直接遍历所有数据，并拼接到一起，不考虑两个迭代器的长度是否相等
    不适合数据量非常大的数据拼接
    '''
    for count, name in zip(length, names):
        print count, name
    # 使用itertools.izip方法适合大数据量的生成
    for count, name in itertools.izip(length, names):
        if count > max:
            max = count
            max_name = name
    print max_name
    print '此时添加了一个新元素：“abcdefghi”,izip无法拼接不同长度的迭代器'
    names.append('abcdefghi')
    for count, name in itertools.izip(length, names):
        if count > max:
            max = count
            max_name = name
    print max_name, name
    # 可以遍历到新添加元素，但是count变量为None
    for count, name in itertools.izip_longest(length, names):
        if count > max:
            max = count
            max_name = name
    print max_name, name, count


def fun2():
    file_path = 'my_test.txt'
    with open(file_path, 'w+') as f:
        f.write(unichr(int('7f51', 16)).encode('utf-8'))
    pass
    with open(file_path, 'r') as f:
        print f.read().decode('utf-8')


def fun3():
    file_path = 'my_test.txt'
    parser = jsonparser.JSONParser()
    # parser.loads('{"a": "\\u7f51\\u6613CC\\"\'"}')
    # parser.dump_file(file_path)
    # print parser.dumps()
    # print parser.dump_dict()
    # print '\"'+'\\u7f51\\u6613CC\\"\''+'\"'
    # print ''.join(['{','"a"',':',u'\"'+'\\u7f51\\u6613CC\\"\''+'\"','}'])
    # parser.loads('{"a": "\\u7f51\\u6613CC\\"\'"}')
    parser.loads('{"a": "\\u7f51\\u6613CC\\"\'"}')
    print parser.dumps()
    # parser.load_file(file_path)
    # print parser.dump_dict()
    # print json.loads('{"\\t":"\\""}')
    # parser.dump_file(file_path)
    # parser.load_file(file_path)


def fun4():
    file_path = 'my_test.txt'
    with open(file_path, 'w+') as f:
        f.write(u'\\"')


if __name__ == '__main__':
    # fun1()
    fun3()
