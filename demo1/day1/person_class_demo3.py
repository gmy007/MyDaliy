# -*- coding: utf-8
class Employee:
    empCount = 0
    __sex = ''  # 私有属性

    def __init__(self, name, salary, sex):
        self.name = name
        self.salary = salary
        self.__sex = sex
        Employee.empCount += 1

    def displayCount(self):
        print('Total Employee {}'.format(self.empCount))

    def displayEmployee(self):
        print('Employee name is {}.\n'
              'Employee salary is {}\n'
              'Employee sex is {}'.format(self.name, self.salary, self.__sex))


sc1 = Employee('gmy', 6000, 'man')
sc2 = Employee('Ljr', 1000000, 'girl')
sc1.displayCount()
sc1.displayEmployee()
sc2.displayEmployee()
sc2.displayCount()


class Gmy(Employee):
    __college = ''
    __haveMarried = False

    def __init__(self, name, salary, sex, college, haveMarried) :
        Employee.__init__(name, salary, sex)
        self.__haveMarried = haveMarried
        self.__college = college

    def work(self):
        print('Gmy is working at wy')

    def displayCount(self):
        Employee.displayCount()
        print('college is {}\t'.format(self.__college))
        print('Gmy has {} got married'.format('' if self.__haveMarried else "not"))



gmy = Gmy('gmy', 6000, 'man', 'CUG', False)
hcx = Gmy('hcx', 6000, 'man', 'dont know', True)
gmy.work()
gmy.displayEmployee()
hcx.displayEmployee()
