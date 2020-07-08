# -*- coding: UTF-8 -*
for num in range(10, 20):
    for i in range(2, num):  # 根据因子迭代
        if num % i == 0:  # 确定第一个因子
            j = num / i  # 计算第二个因子
            print '%d 等于 %d * %d' % (num, i, j)
            break  # 跳出当前循环
    else:  # 循环的 else 部分
        print num, '是一个质数'

count = 0
while count < 5:
    print count, 'is less than 5'
    count += 1
else:
    print '---- over ----'
