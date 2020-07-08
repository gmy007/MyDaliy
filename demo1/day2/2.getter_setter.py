class Person:
    static_attribute = '123'
    __private_attribute = '321'

    @property
    def name(self):
        return self.name;

    @name.setter
    def name(self, value):
        if not isinstance(self.name, str):
            print 'name must be str'
        else:
            self.name = value

    # def __init__(self,static_attribute,private_attribute,name):
    #     self.static_attribute=static_attribute
    #     self.__private_attribute=private_attribute
    #     self.name=name


p1 = Person()
p1.name = 'gmy'
p2 = Person
p2.name = 123
p1.static_attribute = 'static'
print p2.static_attribute
print p1.static_attribute
print p1.name

print '-' * 50


class Student(object):
    count = 0

    # def __new__(cls, *args, **kwargs):
    #     return

    def __init__(self, name):
        self.name = name
        self.count += 1
        Student.count += 1

    @staticmethod
    def static_fun():
        print 'this is static method'


print Student.count

s1 = Student('123')
print s1.count
print Student.count
print Student.static_fun()