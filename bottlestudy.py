import functools

__author__ = 'Jian'

def makelist(data):
    ''' ��װ�������Ϊlist
    :param data:
    :return:
    '''
    if getattr(data, '__iter__', False):
        return list(data)
    elif data:
        return [data]
    else:
        return []

# DictPropertyװ����
class DictProperty(object):
    ''' Property that maps to a key in a local dict-like attribute.
    ӳ�����κ��property��owner class�е�ĳ�������ֵ��attribute
    (����Ҳ��property��attribute�����������ԣ��Ա�ʾ����)
    '''
    def __init__(self, attr, key=None, read_only=False):
        self.attr, self.key, self.read_only = attr, key, read_only

    def __call__(self, func): # �Ե��õķ���ʹ��װ��������װ�εĺ�����__call__��������Ϊ��������
        functools.update_wrapper(self, func, updated=[]) # ��update_wrapper�ķ�����func��__module__��__name__��__doc__����װ�κ��attribute
        # ����ֻ�����ڸ���'__module__', '__name__', '__doc__'
        # ��ס�˴���self.getterӦ�ð�������һ���򵥵����ԣ������汣����װ�εĶ���
        self.getter, self.key = func, self.key or func.__name__
        return self         # ���attribute��DictProperty��ʵ��

    def __get__(self, obj, cls): # ��������Ϊ��װ�κ��ʵ����owner class��ʵ����owner class
        if obj is None:
            return self
        key, storage = self.key, getattr(obj, self.attr)  # self.attr��owner class��һ��attribute
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

# DictPropertyʹ��ʾ�������װ����װ�κ��γɵ�property���޸ĺ󣬻�ı�owner class�а󶨵�attribute��
class sample(object):
    def __init__(self):
        self.config = {}

    @DictProperty('config', 'sample.foo', read_only=True)
    def foo(self):
        return 'foo'

    @DictProperty('config', 'sample.bar', read_only=True)
    def bar(self):
        return 'bar'

# CachedPropertyװ����
# Why use this? Because this is to implement descriptor,for detail information, you can take a look at
# http://docs.python.org/2/reference/datamodel.html#implementing-descriptors
class CachedProperty(object):
    '''ÿ��ʵ��ֻ�ڵ�һ��get��ʱ������property��ֵ��֮�����instance��__dict__
    �У������ʶ����propertyʱ�����__dict__���У����ȷ���__dict__�м�¼��ֵ����
    ��û�У���ִ�б�����property��__get__�ķ�������
    '''
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        # objΪӵ��������ԵĶ���clsΪ������������,��ʱ���objΪself����
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value

# lazy_attributeװ����
# Why use this? Because this is to implement descriptor,for detail information, you can take a look at
# http://docs.python.org/2/reference/datamodel.html#implementing-descriptors
class lazy_attribute(object): # Does not need configuration -> lower-case nameΪ�໺����
    ''' A property that caches itself to the class object.
    ���ڵ�һ�ε��õ�ʱ�򣬰Ѽ���Ľ����Ϊowner class��attribute
    '''
    def __init__(self, func):
        functools.update_wrapper(self, func, updated=[])
        self.getter = func

    def __get__(self, obj, cls):
        value = self.getter(cls)
        setattr(cls, self.__name__, value)
        return value