import sys

__author__ = 'Eugene'

# print(vars())
# print(globals())
# print(locals())

class Test(object):
    def __init__(self):
        self.name = 'Hi'

    def printInfo(self):
        print(self.__doc__)
        print(self.__module__)

# test = Test()
# test.printInfo()

# print(__name__)

py = sys.version_info
py3k = py >= (3,0,0)
print(py)
print(py3k)
