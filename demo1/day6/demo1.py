import os


def fun1():
    print __file__
    print os.path
    print os.path.abspath(__file__)
    print os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    fun1()
