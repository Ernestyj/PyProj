# -*- coding: utf-8 -*-
import unittest

from tools.json_tools import JsonConf
from tools import ROOT_PATH


class TestJsonTools(unittest.TestCase):
    def test_get_json_conf(self):
        conf = JsonConf().get_json_conf(path=ROOT_PATH+'/conf/conf.json')
        print(conf)




