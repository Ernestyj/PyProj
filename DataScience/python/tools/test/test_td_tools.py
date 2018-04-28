# -*- coding: utf-8 -*-
import unittest

from tools.td_tools import Teradata
from tools.json_tools import JsonConf
from tools import ROOT_PATH


class TestTdTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("This setUpClass() method only called once.#****************************************")
        conf = JsonConf().get_json_conf(path=ROOT_PATH + '/conf/conf.json')
        conf_td = conf['teradata']
        tera = Teradata(host=conf_td['JACKAL'], user_name=conf_td['username'], password=conf_td['password'])

    @classmethod
    def tearDownClass(cls):
        print("This tearDownClass() method only called once too.#****************************************")

    def setUp(self):
        print("*****do something before test.Prepare environment.*****")

    def tearDown(self):
        print("*****do something after test.Clean up.*****")

    def _Query(self):
        conf = JsonConf().get_json_conf(path=ROOT_PATH + '/conf/conf.json')
        conf_td = conf['teradata']

        tera = Teradata(host=conf_td['JACKAL'], user_name=conf_td['username'], password=conf_td['password'])
        df = tera.query(query_string='''select * from pp_oap_sing_jyang2_t.test;''')
        print(df)

