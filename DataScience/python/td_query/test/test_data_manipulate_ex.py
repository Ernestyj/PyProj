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

    def _drop_table(self):
        dest_db = "pp_scratch_risk"
        dest_table = "ms_auto_trend_us2_1_3_100_100_1_1_1"
        instance.drop_table(dest_db, dest_table)

    def _transalte_100_63_22_14_1(self):
        rules = [
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C')",
            "(SELLER_CONSUMER_SEG == 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string == '10008') & (amt2 != 'c-1h') & (amt2 != 'e-<50')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)


    def _duplicate_rows_to_new_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_us2_1_3'
        dest_db = "pp_scratch_risk"
        weight_a = 900
        weight_b = 400
        weight_c = 9
        weight_d = 16
        weight_e = 1
        dest_table = "ms_auto_trend_us2_1_3_{}_{}_{}_{}_{}".format(weight_a, weight_b, weight_c, weight_d, weight_e)
        instance.duplicate_rows_to_new_table(src_db, src_table, dest_db, dest_table, weight_a, weight_b, weight_c, weight_d, weight_e)

    def _duplicate_rows_from_bad_and_sample_from_good_into_new_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_us'
        dest_db = "pp_scratch_risk"
        bad_scale = 1
        good_scale = 3

        weight_a = 52
        weight_b = 16
        weight_c = 23
        weight_d = 5
        weight_e = 4
        dest_table = "ms_auto_trend_us_{}_{}__{}_{}_{}_{}_{}_v2".format(bad_scale, good_scale, weight_a, weight_b, weight_c, weight_d, weight_e)
        instance.duplicate_rows_from_bad_and_sample_from_good_into_new_table(src_db, src_table, dest_db, dest_table,
                                                                             bad_scale, good_scale,
                                                                             weight_a, weight_b, weight_c, weight_d, weight_e)

    def _generate_hl_job_json(self):
        training_table = "ms_auto_trend_us2_1_3"
        testing_table = "ms_auto_trend_us_t"
        instance.generate_hl_job_json(training_table, testing_table, template_name='hl_job_template_na.json')

    def _add_weight_col_to_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_us2_1_3'
        # weight_a = 0.312
        # weight_b = 0.140
        # weight_c = 0.011
        # weight_d = 0.011
        # weight_e = 0.001
        weight_a = 10 * 30
        weight_b = 8 * 20
        weight_c = 4.6 * 3
        weight_d = 3.7 * 4
        weight_e = 1 * 1
        instance.add_weight_col_to_table(src_db, src_table, weight_a, weight_b, weight_c, weight_d, weight_e)

    def _update_weight_col_in_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_us2_1_3'
        src_col = 'PMT_USD_AMT'
        instance.update_weight_col_in_table(src_db, src_table, src_col)

    def _update_custom_weight_col_in_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_us2_1_3'
        src_col = 'PMT_USD_AMT'
        instance.update_custom_weight_col_in_table(src_db, src_table, src_col)