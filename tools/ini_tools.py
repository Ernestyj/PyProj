# -*- coding: utf-8 -*-
import os
import ConfigParser


class IniConf():
    def __init__(self):
        pass

    #获取config配置文件
    def getConfig(section, key):
        config = ConfigParser.ConfigParser()
        config.read(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/test.ini') #os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件所在目录
        return config.get(section, key)


print IniConf().getConfig('db', 'dbhost')