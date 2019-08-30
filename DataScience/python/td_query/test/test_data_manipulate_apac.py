# -*- coding: utf-8 -*-
import unittest
import os
import pickle
import pandas as pd
import numpy as np

from td_query import ROOT_PATH
from td_query.data_manipulate import data_manipulate_instance as instance
from teradata import UdaExec


class TestDataManipulateAPAC(unittest.TestCase):
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

    def _calculate(self):
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


    def _transalte_1_1_1_1_1(self):
        rules = [
            "(SELLER_CONSUMER_SEG != 'Y') & (RCVR_CNTRY_CODE == 'C2 ') & (FLOW_FAMILY == 'MS FF Website Payments Standard') & (IS_ULP_TRANS_T_F >= 0.5)",
            "(SELLER_CONSUMER_SEG != 'Y') & (RCVR_CNTRY_CODE == 'C2 ') & (FLOW_FAMILY == 'MS FF Website Payments Standard') & (IS_ULP_TRANS_T_F < 0.5) & (SNDR_CNTRY_CODE != 'FR ') & (SUB_FLOW != 'MS Subscription') & (SNDR_CNTRY_CODE != 'ES ') & (SNDR_CNTRY_CODE == 'US ') & (SUB_FLOW != 'MS PayPal Cart') & (SUB_FLOW != 'MS Mobile Shopping Cart Upload') & (dof_bin == 'e->1y') & (amt2 != 'a-1k') & (SUB_FLOW == 'MS Single Line Payment') & (SELLER_CONSUMER_SEG == 'C')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_100_63_22_14_1(self):
        rules = [
            "(SUB_FLOW != 'MS MassPay') & (IS_ULP_TRANS_T_F >= 0.5) & (SNDR_CNTRY_CODE != 'AU ') & (amt2 != 'a-1k') & (SNDR_CNTRY_CODE != 'VN ') & (RCVR_CNTRY_CODE != 'NZ ') & (RCVR_CNTRY_CODE != 'JP ') & (SNDR_CNTRY_CODE != 'C2 ') & (RCVR_CNTRY_CODE != 'SG ') & (amt2 != 'e-<50') & (SNDR_CNTRY_CODE != 'HK ') & (dof_bin != 'b-30') & (SUB_FLOW != 'MS Shopping Cart Upload') & (SNDR_CNTRY_CODE != 'ES ') & (SUB_FLOW != 'MS Mobile Shopping Cart Upload')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_637_64_22_14_1(self):
        rules = [
            "(SUB_FLOW != 'MS MassPay') & (SNDR_CNTRY_CODE == 'US ') & (FLOW_FAMILY == 'MS FF Website Payments Standard') & (amt2 == 'b-5h') & (RCVR_CNTRY_CODE != 'TH ') & (RCVR_CNTRY_CODE != 'JP ') & (IS_ULP_TRANS_T_F >= 0.5)",
            "(SUB_FLOW != 'MS MassPay') & (SNDR_CNTRY_CODE != 'US ') & (RCVR_CNTRY_CODE == 'C2 ') & (IS_ULP_TRANS_T_F >= 0.5) & (SNDR_CNTRY_CODE != 'ES ') & (amt2 != 'e-<50')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_74_16_5_4_1(self):
        rules = [
            "(FLOW_FAMILY == 'MS FF Website Payments Standard') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'a-1k') & (RCVR_CNTRY_CODE != 'VN ') & (SNDR_CNTRY_CODE != 'AU ') & (amt2 != 'e-<50') & (RCVR_CNTRY_CODE != 'NZ ') & (dof_bin != 'b-30') & (RCVR_CNTRY_CODE != 'MY ') & (SNDR_CNTRY_CODE != 'ES ')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_637_64_11_8_1(self):
        rules = [
            "(FLOW_FAMILY == 'MS FF Website Payments Standard') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'a-1k') & (SNDR_CNTRY_CODE != 'VN ') & (amt2 == 'b-5h')"
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_637_63_22_14_1(self):
        rules = [
            "(FLOW_FAMILY == 'MS FF Website Payments Standard') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'a-1k') & (SNDR_CNTRY_CODE != 'VN ') & (amt2 == 'b-5h')"
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_100_64_11_8_1(self):
        rules = [
            "(FLOW_FAMILY == 'MS FF Website Payments Standard') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'a-1k') & (SNDR_CNTRY_CODE != 'VN ') & (amt2 == 'b-5h')"
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_100_64_22_14_1(self):
        rules = [
            "(FLOW_FAMILY == 'MS FF Website Payments Standard') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'a-1k') & (SNDR_CNTRY_CODE != 'VN ') & (amt2 == 'b-5h')"
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_1000_500_100_50_1(self):
        rules = [
            "(SUB_FLOW != 'MS MassPay') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'a-1k') & (SNDR_CNTRY_CODE != 'AU ') & (SNDR_CNTRY_CODE != 'VN ') & (RCVR_CNTRY_CODE != 'NZ ') & (RCVR_CNTRY_CODE != 'JP ') & (RCVR_CNTRY_CODE != 'SG ') & (SNDR_CNTRY_CODE != 'C2 ') & (dof_bin != 'b-30') & (amt2 == 'b-5h')"
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_1_85_7_4_5(self):
        rules = [
            "(IS_ULP_TRANS_T_F >= 0.5) & (amt2 == 'b-5h') & (FLOW_FAMILY == 'MS FF Website Payments Standard')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_tpv(self):
        rules = [
            "(FLOW_FAMILY == 'MS FF Website Payments Standard') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'a-1k') & (RCVR_CNTRY_CODE != 'VN ') & (SNDR_CNTRY_CODE != 'AU ') & (amt2 != 'e-<50') & (dof_bin != 'b-30') & (RCVR_CNTRY_CODE != 'NZ ') & (RCVR_CNTRY_CODE != 'MY ') & (SNDR_CNTRY_CODE != 'ES ') & (amt2 != 'c-1h') & (SNDR_CNTRY_CODE != 'GB ')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_tpv2(self):
        rules = [
            "(SUB_FLOW != 'MS MassPay') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'a-1k') & (SNDR_CNTRY_CODE != 'AU ') & (RCVR_CNTRY_CODE != 'VN ') & (RCVR_CNTRY_CODE != 'NZ ') & (RCVR_CNTRY_CODE != 'JP ') & (RCVR_CNTRY_CODE != 'SG ') & (amt2 != 'e-<50') & (SNDR_CNTRY_CODE != 'C2 ') & (dof_bin != 'b-30') & (SNDR_CNTRY_CODE != 'HK ') & (amt2 == 'b-5h')"
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_mix(self):
        rules = [
            "(FLOW_FAMILY == 'MS FF Website Payments Standard') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'a-1k') & (SNDR_CNTRY_CODE != 'VN ') & (SNDR_CNTRY_CODE != 'AU ') & (RCVR_CNTRY_CODE != 'NZ ') & (dof_bin != 'b-30') & (amt2 != 'e-<50') & (RCVR_CNTRY_CODE != 'MY ') & (SNDR_CNTRY_CODE != 'ES ') & (SUB_FLOW != 'MS Shopping Cart Upload')"
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _duplicate_rows_to_new_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_apac_off_ebay_non_ep_consumer_Day35_trend_month_2017_11_train'
        dest_db = "pp_scratch_risk"
        weight_a = 100
        weight_b = 100
        weight_c = 100
        weight_d = 100
        weight_e = 100
        dest_table = "ms_auto_trend_apac_1_3_{}_{}_{}_{}_{}".format(weight_a, weight_b, weight_c, weight_d, weight_e)
        dest_table = "ms_auto_trend_apac_off_ebay_non_ep_consumer_Day35_trend_month_2017_11_train_{}_{}_{}_{}_{}".format(weight_a, weight_b, weight_c, weight_d, weight_e)
        instance.duplicate_rows_to_new_table(src_db, src_table, dest_db, dest_table, weight_a, weight_b, weight_c, weight_d, weight_e)

    def _duplicate_rows_from_bad_and_sample_from_good_into_new_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_apac'
        dest_db = "pp_scratch_risk"
        bad_scale = 1
        good_scale = 3

        weight_a = 1
        weight_b = 85
        weight_c = 7
        weight_d = 4
        weight_e = 3
        dest_table = "ms_auto_trend_apac_{}_{}__{}_{}_{}_{}_{}_v2".format(bad_scale, good_scale, weight_a, weight_b, weight_c, weight_d, weight_e)
        instance.duplicate_rows_from_bad_and_sample_from_good_into_new_table(src_db, src_table, dest_db, dest_table,
                                                                             bad_scale, good_scale,
                                                                             weight_a, weight_b, weight_c, weight_d, weight_e)

    def _generate_hl_job_json(self):
        training_table = "ms_auto_trend_apac_1_3__1_85_7_4_3_v2"
        testing_table = "ms_auto_trend_apac_t"
        instance.generate_hl_job_json(training_table, testing_table)

    def _add_weight_col_to_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_apac_1_3'
        # weight_a = 0.312
        # weight_b = 0.140
        # weight_c = 0.011
        # weight_d = 0.011
        # weight_e = 0.001
        weight_a = 10 * 74
        weight_b = 8 * 16
        weight_c = 4.6 * 5
        weight_d = 3.7 * 4
        weight_e = 1 * 1
        instance.add_weight_col_to_table(src_db, src_table, weight_a, weight_b, weight_c, weight_d, weight_e)

    def _update_weight_col_in_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_apac_1_3'
        src_col = 'PMT_USD_AMT'
        instance.update_weight_col_in_table(src_db, src_table, src_col)

    def _update_custom_weight_col_in_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_apac_1_3'
        src_col = 'PMT_USD_AMT'
        instance.update_custom_weight_col_in_table(src_db, src_table, src_col)