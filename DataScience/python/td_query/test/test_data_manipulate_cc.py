# -*- coding: utf-8 -*-
import unittest
import os
import pickle
import pandas as pd
import numpy as np

from td_query import ROOT_PATH
from td_query.data_manipulate_cc import data_manipulate_cc_instance as instance
from teradata import UdaExec


class TestDataManipulateCC(unittest.TestCase):
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

    # def _transalte_100_63_22_14_1(self):
    #     rules = [
    #         "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C')",
    #         "(SELLER_CONSUMER_SEG == 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string == '10008') & (amt2 != 'c-1h') & (amt2 != 'e-<50')",
    #     ]
    #     result = instance.translate_hyperloop_rules_to_sql(rules)
    #     print(result)

    def _get_all_bad_and_sample_from_good_into_new_table(self):
        # src_db = "pp_scratch_risk"
        # src_db = "PP_OAP_ROM_T"
        src_db = "PP_OAP_SING_JYANG2_T"
        # src_table = 'cc_hl_base_case1_train'
        src_table = 'cc_hyperloop_base_cg_sel_train'
        # dest_db = "pp_scratch_risk"
        dest_db = "PP_OAP_SING_JYANG2_T"
        bad_scale = 1
        good_scale = 3

        # dest_table = "cc_hl_case1_train_{}_{}".format(bad_scale, good_scale,)
        dest_table = "cc_hyperloop_base_cg_sel_train_{}_{}".format(bad_scale, good_scale,)
        instance.get_all_bad_and_sample_from_good_into_new_table(src_db, src_table, dest_db, dest_table, bad_scale, good_scale,)

    def _get_all_bad_and_sample_from_good_into_new_table_reverse(self):
        # src_db = "pp_scratch_risk"
        # src_db = "PP_OAP_ROM_T"
        src_db = "PP_OAP_SING_JYANG2_T"
        # src_table = 'cc_hl_base_case1_train'
        src_table = 'cc_hyperloop_base_cg_sel_train'
        # dest_db = "pp_scratch_risk"
        dest_db = "PP_OAP_SING_JYANG2_T"
        bad_scale = 1
        good_scale = 3

        # dest_table = "cc_hl_case1_train_{}_{}".format(bad_scale, good_scale,)
        dest_table = "cc_hyperloop_base_cg_sel_train_{}_{}".format(bad_scale, good_scale,)
        instance.get_all_bad_and_sample_from_good_into_new_table_reverse(src_db, src_table, dest_db, dest_table, bad_scale, good_scale,)

    # def _generate_hl_job_json(self):
    #     training_table = "ms_auto_trend_us2_1_3"
    #     testing_table = "ms_auto_trend_us_t"
    #     instance.generate_hl_job_json(training_table, testing_table, template_name='hl_job_template_na.json')

    # def _update_weight_col_in_table(self):
    #     src_db = "pp_scratch_risk"
    #     src_table = 'ms_auto_trend_us2_1_3'
    #     src_col = 'PMT_USD_AMT'
    #     instance.update_weight_col_in_table(src_db, src_table, src_col)

    def _update_custom_weight_col_in_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_us2_1_3'
        src_col = 'PMT_USD_AMT'
        instance.update_custom_weight_col_in_table(src_db, src_table, src_col)

    def _add_is_cc_bad_col_in_table(self):
        src_db = "PP_OAP_ROM_T"
        src_table = 'cc_hl_base_case2_test'
        instance.add_is_cc_bad_col_in_table(src_db, src_table)

    def _add_is_cc_bad_reverse_col_in_table(self):
        src_db = "PP_OAP_SING_JYANG2_T"
        src_table = 'cc_hyperloop_base_cg_sel_test'
        instance.add_is_cc_bad_reverse_col_in_table(src_db, src_table)

    def _get_all_bad_and_sample_from_good_into_new_table_and_append_custom_weight_col(self):
        # src_db = "PP_OAP_ROM_T"
        src_db = "PP_OAP_SING_JYANG2_T"
        # src_table = 'cc_hl_base_case2_train'
        src_table = 'cc_hyperloop_base_cg_sel_test'
        # dest_db = "PP_OAP_ROM_T"
        dest_db = "PP_OAP_SING_JYANG2_T"
        bad_scale = 1
        good_scale = 3

        dest_table = "cc_hl_case2_train_{}_{}".format(bad_scale, good_scale,)
        instance.get_all_bad_and_sample_from_good_into_new_table(src_db, src_table, dest_db, dest_table,
                                                                 bad_scale, good_scale,)
        src_col = 'usd_amt'
        instance.update_custom_weight_col_in_table(src_db, src_table=dest_table, src_col=src_col)

        instance.add_is_cc_bad_col_in_table(src_db, src_table=dest_table)
