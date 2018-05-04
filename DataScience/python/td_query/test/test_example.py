# -*- coding: utf-8 -*-
import unittest
import os
import pickle

from td_query import ROOT_PATH
from td_query.td_query_base import TeradataQueryBase


instance = TeradataQueryBase(conf_path=os.path.join(ROOT_PATH, 'conf/conf.json'), teradata_platform='JACKAL')


class TestExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("**************************************** setUpClass ****************************************")
        instance.init()
        print(instance.teradata)

    @classmethod
    def tearDownClass(cls):
        print("************************************** tearDownClass ***************************************")

    def setUp(self):
        print("****** setUp *******")

    def tearDown(self):
        print("***** tearDown *****")

    def _example(self):
        df = instance.query_sample()
        # with open(ROOT_PATH + '/external/df_dispatch_bna.pickle', 'wb') as f: # save
        #     pickle.dump(df, f)
        print(df)

