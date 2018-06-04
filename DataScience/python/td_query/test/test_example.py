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
        # df = instance.query_sample()
        # with open(ROOT_PATH + '/external/df_dispatch_bna.pickle', 'wb') as f: # save
        #     pickle.dump(df, f)
        # print(df)
        print('example')
        for i in range(1,1):
            print(i)
        pass

    def _query_count(self):
        # df = instance.query('''select count(*) from pp_scratch_risk.ms_auto_trend_us2_1_3''')
        df = instance.query('''select count(*) from PP_OAP_SING_JYANG2_T.test''')
        print(df.iloc[0, 0])

    def _query_multi(self):
        df = instance.teradata.execute('''
        update PP_OAP_SING_JYANG2_T.test SET name=(case when id=1 then 'J' when id=2 then 'E' else 'Else' end);
        ''')

        print(df)

    def test_get_months(self):
        print(TestExample.get_months(3))

    @staticmethod
    def get_month_str(year, month):
        if month < 10:
            return str(year) + '0' + str(month)
        else:
            return str(year) + str(month)

    @staticmethod
    def get_months(time_period):
        import datetime
        import math
        if time_period == 'all':
            today = datetime.date.today()
            start_date = datetime.date(2015, 6, 1)
            months = (today.year - start_date.year) * 12 + today.month - start_date.month + 1
            year = today.year
            month = today.month
        else:
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            months = int(time_period) + 1
        ret_str = TestExample.get_month_str(year, month)
        for i in range(2, months):
            year_delta = int(math.ceil((month - i) / 12))
            cur_month = (month - i) % 12 + 1
            ret_str += ',' + TestExample.get_month_str(year + year_delta, cur_month)
        return ret_str
