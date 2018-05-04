# -*- coding: utf-8 -*-
import unittest
import os
import pickle
import pandas as pd
import numpy as np

from td_query import ROOT_PATH
from td_query.data_manipulate import data_manipulate_instance as instance
from teradata import UdaExec


class TestDataManipulate(unittest.TestCase):
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

    def test_calculate(self):
        def percent(x, y):
            return round(x/y*100, 2)
        total = 115554
        print(
            percent(2877, total),
            percent(3909, total),
            percent(23030, total),
            percent(18840, total),
            percent(66898, total),
        )

    def _query(self):
        query = '''select top 10 * from pp_scratch_risk.ms_auto_trend_us_bad;'''
        df = instance.query(query)
        print(df)

    def _query_table_schema(self):
        dest_db = "pp_scratch_risk"
        dest_table = "ms_auto_trend_us2_1_3_100_100_1_1_1"
        result_cursor = instance.teradata.execute("show select * from {}.{};".format(dest_db, dest_table))
        last_row = result_cursor.fetchall()
        print(last_row)

    def _query_table_top_rows(self):
        table = "pp_scratch_risk.ms_auto_trend_us_bad"
        df = instance.query_table_top_rows(table)
        print(df)

    def _insert_to_table(self):
        cols = ['id', 'name', 'phone']
        data = [
            (1, "jy", "1888"),
            (2, "jy", "1999"),
        ]
        df = pd.DataFrame.from_records(data, columns=cols)
        df_name_is_jy = df[df['name']=='jy']
        df = df.append([df_name_is_jy]*2, ignore_index=True)
        print(pd.concat([df_name_is_jy]*2, ignore_index=True))
        # print(df)
        print("-------------")
        database = "pp_scratch_risk"
        table = "jy_test"
        instance.insert_to_table(df, database, table)
        query = '''select * from {}.{};'''.format(database, table)
        result_df = instance.query(query)
        print(result_df)

    def _create_table_from_src_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_us2_1_3'
        dest_db = "pp_scratch_risk"
        dest_table = "ms_auto_trend_us2_1_3_100_100_1_1_1"
        instance.create_table_from_src_table_schema(src_db, src_table, dest_db, dest_table)

    def _drop_table(self):
        dest_db = "pp_scratch_risk"
        dest_table = "ms_auto_trend_us2_1_3_100_100_1_1_1"
        instance.drop_table(dest_db, dest_table)

    def test_duplicate_rows_to_new_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_us2_1_3'
        dest_db = "pp_scratch_risk"
        weight_a = 20
        weight_b = 20
        weight_c = 1
        weight_d = 1
        weight_e = 1
        dest_table = "ms_auto_trend_us2_1_3_{}_{}_{}_{}_{}".format(weight_a, weight_b, weight_c, weight_d, weight_e)
        instance.duplicate_rows_to_new_table(src_db, src_table, dest_db, dest_table, weight_a, weight_b, weight_c, weight_d, weight_e)