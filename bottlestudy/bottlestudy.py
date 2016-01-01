import functools

__author__ = 'Jian'

def makelist(data):
    ''' 包装任意对象为list
    :param data:
    :return:
    '''
    if getattr(data, '__iter__', False):
        return list(data)
    elif data:
        return [data]
    else:
        return []

# DictProperty装饰器
class DictProperty(object):
    ''' Property that maps to a key in a local dict-like attribute.
    映射修饰后的property到owner class中的某个类似字典的attribute
    (后文也用property和attribute，而不用属性，以表示区别)
    '''
    def __init__(self, attr, key=None, read_only=False):
        self.attr, self.key, self.read_only = attr, key, read_only

    def __call__(self, func): # 以调用的方法使用装饰器，则被装饰的函数在__call__方法里作为参数传入
        functools.update_wrapper(self, func, updated=[]) # 用update_wrapper的方法把func的__module__，__name__，__doc__赋给装饰后的attribute
        # 现在只是用于复制'__module__', '__name__', '__doc__'
        # 记住此处的self.getter应该把它当作一个简单的属性，它里面保存着装饰的对象
        self.getter, self.key = func, self.key or func.__name__
        return self         # 这个attribute是DictProperty的实例

    def __get__(self, obj, cls): # 参数依次为被装饰后的实例，owner class的实例，owner class
        if obj is None:
            return self
        key, storage = self.key, getattr(obj, self.attr)  # self.attr是owner class的一个attribute
        if key not in storage:
            storage[key] = self.getter(obj)
        return storage[key]

    def __set__(self, obj, value):
        if self.read_only:
            raise AttributeError("Read-Only property.")
        getattr(obj, self.attr)[self.key] = value

    def __delete__(self, obj):
        if self.read_only:
            raise AttributeError("Read-Only property.")
        del getattr(obj, self.attr)[self.key]

# DictProperty使用示例（这个装饰器装饰后形成的property在修改后，会改变owner class中绑定的attribute）
class sample(object):
    def __init__(self):
        self.config = {}

    @DictProperty('config', 'sample.foo', read_only=True)
    def foo(self):
        return 'foo'

    @DictProperty('config', 'sample.bar', read_only=True)
    def bar(self):
        return 'bar'

# CachedProperty装饰器
# Why use this? Because this is to implement descriptor,for detail information, you can take a look at
# http://docs.python.org/2/reference/datamodel.html#implementing-descriptors
class CachedProperty(object):
    '''每个实例只在第一次get的时候计算的property的值，之后存在instance的__dict__
    中（当访问对象的property时，如果__dict__中有，则先返回__dict__中记录的值，如
    果没有，则执行被访问property的__get__的方法。）
    '''
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        # obj为拥有这个属性的对象，cls为这个对象的类型,此时这个obj为self本身
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value

# lazy_attribute装饰器
# Why use this? Because this is to implement descriptor,for detail information, you can take a look at
# http://docs.python.org/2/reference/datamodel.html#implementing-descriptors
class lazy_attribute(object): # Does not need configuration -> lower-case name为类缓存结果
    ''' A property that caches itself to the class object.
    会在第一次调用的时候，把计算的结果设为owner class的attribute
    '''
    def __init__(self, func):
        functools.update_wrapper(self, func, updated=[])
        self.getter = func

    def __get__(self, obj, cls):
        value = self.getter(cls)
        setattr(cls, self.__name__, value)
        return value