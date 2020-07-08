for i in range(5):
    print i


def triangles():
    list1 = [1]
    while 1:
        list2 = [1]
        yield list1
        for i in range(len(list1) - 1):
            list2.append(list1[i] + list1[i + 1])
        list2.append(1)
        list1 = list2


z = triangles()
for i in range(10):
    print z.next()
