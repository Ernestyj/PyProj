# -*- coding: utf-8 -*-
import unittest
import os
import pickle
import pandas as pd
import numpy as np

from td_query import ROOT_PATH
from td_query.data_manipulate import data_manipulate_instance as instance
from teradata import UdaExec


class TestDataManipulateLATAM(unittest.TestCase):
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
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SELLER_SEG == '04 YS') & (dof_bin != 'a-7') & (RCVR_CNTRY_CODE == 'CL ') & (SUB_FLOW == 'MS Send Money Internal')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (dof_bin != 'd-1y') & (RCVR_CNTRY_CODE != 'PA ') & (dof_bin == 'c-90') & (SNDR_CNTRY_CODE == 'CO ') & (RCVR_CNTRY_CODE != 'MX ') & (RCVR_CNTRY_CODE == 'EC ')",
            "(dof_bin == 'e->1y') & (SNDR_CNTRY_CODE != 'CL ') & (RCVR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'PE ') & (amt2 == 'a-1k') & (RCVR_CNTRY_CODE == 'PE ')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SELLER_SEG == '04 YS') & (dof_bin == 'a-7') & (IS_ULP_TRANS_T_F < 0.5) & (SUB_FLOW != 'MS Send Money Internal') & (RCVR_CNTRY_CODE != 'VE ')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (dof_bin == 'd-1y') & (RCVR_CNTRY_CODE != 'UY ') & (RCVR_CNTRY_CODE != 'JM ') & (SNDR_CNTRY_CODE != 'US ') & (amt2 != 'b-5h') & (SELLER_CONSUMER_SEG == 'T') & (RCVR_CNTRY_CODE == 'MX ') & (SNDR_CNTRY_CODE == 'MX ') & (SUB_FLOW == 'MS Send Money Internal') & (amt2 != 'e-<50')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (SELLER_CONSUMER_SEG != 'T') & (SUB_FLOW != 'MS Send Money Internal') & (amt2 == 'e-<50') & (SELLER_SEG == '04 YS') & (dof_bin != 'a-7')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SELLER_SEG == '04 YS') & (dof_bin != 'a-7') & (RCVR_CNTRY_CODE == 'CL ') & (SUB_FLOW != 'MS Send Money Internal')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_1_1_1_1_1_one(self):
        rules = [
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (SELLER_CONSUMER_SEG != 'T') & (SUB_FLOW == 'MS Send Money Internal') & (SELLER_SEG == '04 YS')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_1_1_1_1_1_one_1_on_1(self):
        rules = [
            "(dof_bin != 'e->1y') & (SELLER_SEG == '04 YS') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (RCVR_CNTRY_CODE == 'CL ')"
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_100_63_22_14_1_v2(self):
        rules = [
            "(dof_bin == 'a-7') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (RCVR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'UY ') & (SUB_FLOW == 'MS Mobile Money Request - Invoicing') & (RCVR_CNTRY_CODE == 'PE ')",
            "(dof_bin == 'a-7') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (IS_ULP_TRANS_T_F < 0.5) & (RCVR_CNTRY_CODE == 'CL ') & (SUB_FLOW == 'MS Send Money Internal') & (amt2 != 'c-1h')",
            "(dof_bin == 'a-7') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (RCVR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'UY ') & (RCVR_CNTRY_CODE == 'UY ') & (amt2 == 'e-<50') & (SUB_FLOW == 'MS Send Money Internal')",
            "(dof_bin != 'a-7') & (RCVR_CNTRY_CODE == 'CL ') & (SELLER_SEG == '04 YS') & (dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SUB_FLOW == 'MS Send Money Internal') & (dof_bin == 'b-30')",
            "(dof_bin != 'a-7') & (RCVR_CNTRY_CODE != 'CL ') & (dof_bin != 'b-30') & (dof_bin != 'e->1y') & (RCVR_CNTRY_CODE != 'VE ') & (RCVR_CNTRY_CODE != 'PA ') & (SNDR_CNTRY_CODE != 'CO ') & (RCVR_CNTRY_CODE != 'JM ') & (RCVR_CNTRY_CODE == 'UY ') & (amt2 != 'e-<50') & (SELLER_SEG == '04 YS') & (SNDR_CNTRY_CODE != 'PE ') & (SNDR_CNTRY_CODE != 'UY ') & (SNDR_CNTRY_CODE == 'BR ')",
            "(dof_bin == 'a-7') & (SNDR_CNTRY_CODE == 'VE ') & (SUB_FLOW == 'MS Send Money Internal') & (IS_ULP_TRANS_T_F < 0.5) & (amt2 != 'c-1h') & (RCVR_CNTRY_CODE != 'AR ') & (RCVR_CNTRY_CODE != 'CO ') & (RCVR_CNTRY_CODE != 'MX ') & (amt2 == 'e-<50')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_1000_500_100_50_1(self):
        rules = [
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 != 'a-1k') & (SUB_FLOW == 'MS Send Money Internal') & (SELLER_CONSUMER_SEG != 'T') & (SELLER_CONSUMER_SEG == 'Y') & (SELLER_SEG == '04 YS') & (dof_bin != 'b-30') & (amt2 == 'd-50') & (dof_bin != 'd-1y')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SUB_FLOW != 'MS Send Money Internal') & (dof_bin == 'a-7') & (SUB_FLOW != 'MS Mobile Money Request') & (RCVR_CNTRY_CODE != 'AR ') & (RCVR_CNTRY_CODE != 'PE ') & (SUB_FLOW == 'MS Mobile Cons App Send Money - Commercial') & (amt2 != 'c-1h') & (RCVR_CNTRY_CODE != 'VE ') & (amt2 == 'e-<50')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SUB_FLOW == 'MS Send Money Internal') & (SELLER_SEG == '04 YS') & (amt2 != 'b-5h') & (RCVR_CNTRY_CODE == 'CL ') & (dof_bin != 'a-7') & (amt2 != 'c-1h')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (SNDR_CNTRY_CODE != 'PE ') & (dof_bin == 'a-7') & (SNDR_CNTRY_CODE != 'BR ') & (SNDR_CNTRY_CODE != 'DO ') & (RCVR_CNTRY_CODE != 'VE ') & (RCVR_CNTRY_CODE != 'HN ') & (RCVR_CNTRY_CODE != 'EC ') & (SNDR_CNTRY_CODE == 'MX ') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'c-1h') & (amt2 == 'e-<50') & (SUB_FLOW == 'MS Send Money Internal')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 != 'a-1k') & (SUB_FLOW == 'MS Send Money Internal') & (SELLER_CONSUMER_SEG != 'T') & (SELLER_CONSUMER_SEG == 'Y') & (SELLER_SEG == '04 YS') & (dof_bin != 'b-30') & (amt2 != 'd-50') & (IS_ULP_TRANS_T_F < 0.5)",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SUB_FLOW != 'MS Send Money Internal') & (dof_bin != 'a-7') & (RCVR_CNTRY_CODE == 'CL ') & (SELLER_CONSUMER_SEG != 'Y') & (amt2 == 'd-50') & (SELLER_SEG == '04 YS')"
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_100_63_22_14_1(self):
        rules = [
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (amt2 != 'a-1k') & (SELLER_CONSUMER_SEG != 'T') & (SUB_FLOW == 'MS Send Money Internal') & (SELLER_CONSUMER_SEG == 'Y') & (SELLER_SEG == '04 YS') & (dof_bin != 'b-30') & (amt2 == 'd-50') & (dof_bin != 'd-1y')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (dof_bin == 'a-7') & (RCVR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'BR ') & (SNDR_CNTRY_CODE != 'DO ') & (RCVR_CNTRY_CODE != 'HN ') & (RCVR_CNTRY_CODE != 'EC ') & (SNDR_CNTRY_CODE != 'MX ') & (RCVR_CNTRY_CODE == 'UY ') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial') & (amt2 == 'e-<50') & (SNDR_CNTRY_CODE == 'UY ')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (dof_bin != 'a-7') & (SNDR_CNTRY_CODE != 'PE ') & (SNDR_CNTRY_CODE != 'JM ') & (SNDR_CNTRY_CODE != 'CO ') & (SNDR_CNTRY_CODE == 'US ') & (SUB_FLOW == 'MS Mobile Money Request - Invoicing') & (RCVR_CNTRY_CODE == 'PE ')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (dof_bin != 'a-7') & (SNDR_CNTRY_CODE != 'PE ') & (SNDR_CNTRY_CODE != 'JM ') & (SNDR_CNTRY_CODE == 'CO ') & (SELLER_SEG == '04 YS') & (amt2 != 'a-1k') & (SUB_FLOW == 'MS Send Money Internal') & (amt2 == 'c-1h') & (RCVR_CNTRY_CODE != 'EC ') & (RCVR_CNTRY_CODE == 'PE ') & (dof_bin != 'b-30')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SELLER_SEG == '04 YS') & (SUB_FLOW == 'MS Send Money Internal') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (dof_bin != 'a-7')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (amt2 != 'a-1k') & (SELLER_CONSUMER_SEG != 'T') & (SUB_FLOW == 'MS Send Money Internal') & (SELLER_CONSUMER_SEG == 'Y') & (SELLER_SEG == '04 YS') & (dof_bin != 'b-30') & (amt2 != 'd-50')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_46_27_5_5_1(self):
        rules = [
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (dof_bin == 'a-7') & (RCVR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'BR ') & (SNDR_CNTRY_CODE != 'DO ') & (SNDR_CNTRY_CODE != 'HN ') & (SNDR_CNTRY_CODE == 'UY ') & (amt2 == 'e-<50')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 != 'a-1k') & (SELLER_CONSUMER_SEG != 'T') & (SUB_FLOW == 'MS Send Money Internal') & (amt2 == 'd-50') & (dof_bin != 'b-30')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 != 'a-1k') & (SELLER_CONSUMER_SEG != 'T') & (SUB_FLOW == 'MS Send Money Internal') & (amt2 != 'd-50') & (SELLER_SEG == '04 YS') & (dof_bin != 'd-1y') & (SELLER_CONSUMER_SEG == 'Y')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SELLER_SEG == '04 YS') & (SUB_FLOW == 'MS Send Money Internal') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_312_140_11_11_1(self):
        rules = [
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (SNDR_CNTRY_CODE != 'US ') & (amt2 != 'b-5h') & (dof_bin == 'a-7') & (SNDR_CNTRY_CODE != 'BR ') & (SNDR_CNTRY_CODE != 'DO ') & (RCVR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'MX ') & (IS_ULP_TRANS_T_F < 0.5) & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial') & (amt2 != 'a-1k') & (amt2 != 'e-<50') & (RCVR_CNTRY_CODE == 'PE ')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (amt2 != 'a-1k') & (RCVR_CNTRY_CODE == 'CL ') & (SUB_FLOW == 'MS Send Money Internal') & (SELLER_CONSUMER_SEG != 'T') & (SELLER_CONSUMER_SEG == 'Y') & (SELLER_SEG == '04 YS') & (dof_bin != 'b-30') & (amt2 == 'd-50')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (SNDR_CNTRY_CODE != 'US ') & (amt2 != 'b-5h') & (dof_bin == 'a-7') & (SNDR_CNTRY_CODE != 'BR ') & (SNDR_CNTRY_CODE != 'DO ') & (RCVR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'MX ') & (amt2 != 'a-1k') & (RCVR_CNTRY_CODE == 'UY ') & (SNDR_CNTRY_CODE != 'DE ') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial') & (SNDR_CNTRY_CODE != 'AR ')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SELLER_SEG == '04 YS') & (SUB_FLOW == 'MS Send Money Internal') & (amt2 != 'b-5h') & (RCVR_CNTRY_CODE == 'CL ') & (dof_bin != 'a-7')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (amt2 != 'a-1k') & (RCVR_CNTRY_CODE == 'CL ') & (SUB_FLOW == 'MS Send Money Internal') & (SELLER_CONSUMER_SEG != 'T') & (SELLER_CONSUMER_SEG == 'Y') & (SELLER_SEG == '04 YS') & (dof_bin != 'b-30') & (amt2 != 'd-50')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_7_4_5_3_6(self):
        rules = [
            "(dof_bin == 'a-7') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (SUB_FLOW == 'MS Send Money Internal') & (IS_ULP_TRANS_T_F < 0.5) & (RCVR_CNTRY_CODE == 'CL ')",
            "(dof_bin == 'a-7') & (SNDR_CNTRY_CODE == 'VE ') & (SUB_FLOW == 'MS Send Money Internal') & (IS_ULP_TRANS_T_F < 0.5) & (RCVR_CNTRY_CODE != 'AR ') & (amt2 != 'c-1h') & (RCVR_CNTRY_CODE != 'CO ') & (RCVR_CNTRY_CODE != 'PE ') & (RCVR_CNTRY_CODE != 'MX ') & (RCVR_CNTRY_CODE != 'CL ')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_tpv(self):
        rules = [
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE != 'CL ') & (dof_bin == 'd-1y') & (RCVR_CNTRY_CODE != 'PE ') & (SNDR_CNTRY_CODE != 'IL ') & (SNDR_CNTRY_CODE != 'US ') & (RCVR_CNTRY_CODE != 'AR ') & (RCVR_CNTRY_CODE != 'BR ') & (SUB_FLOW != 'MS Money Request') & (SNDR_CNTRY_CODE == 'MX ') & (SUB_FLOW == 'MS Mobile Cons App Send Money - Commercial') & (RCVR_CNTRY_CODE == 'GT ')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (SUB_FLOW == 'MS Send Money Internal') & (amt2 != 'a-1k') & (SELLER_SEG == '04 YS') & (RCVR_CNTRY_CODE != 'PE ') & (amt2 != 'c-1h') & (RCVR_CNTRY_CODE == 'CL ') & (dof_bin != 'c-90') & (dof_bin == 'a-7') & (IS_ULP_TRANS_T_F < 0.5)",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SELLER_SEG == '04 YS') & (amt2 != 'b-5h') & (SUB_FLOW == 'MS Send Money Internal') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 == 'c-1h') & (SELLER_CONSUMER_SEG == 'Y') & (dof_bin == 'd-1y')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SELLER_SEG == '04 YS') & (amt2 != 'b-5h') & (SUB_FLOW == 'MS Send Money Internal') & (RCVR_CNTRY_CODE != 'CL ') & (dof_bin == 'a-7') & (amt2 != 'c-1h') & (RCVR_CNTRY_CODE != 'AR ') & (amt2 != 'a-1k') & (IS_ULP_TRANS_T_F < 0.5)",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_tpv2(self):
        rules = [
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (amt2 != 'b-5h') & (RCVR_CNTRY_CODE != 'DO ') & (RCVR_CNTRY_CODE != 'BR ') & (RCVR_CNTRY_CODE != 'MX ') & (SELLER_CONSUMER_SEG != 'T') & (amt2 != 'a-1k') & (SELLER_SEG == '04 YS') & (RCVR_CNTRY_CODE != 'PE ') & (RCVR_CNTRY_CODE != 'CR ') & (amt2 != 'c-1h') & (RCVR_CNTRY_CODE == 'CL ') & (dof_bin != 'c-90')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (SELLER_SEG == '04 YS') & (amt2 != 'b-5h') & (RCVR_CNTRY_CODE != 'CO ') & (RCVR_CNTRY_CODE != 'MX ') & (RCVR_CNTRY_CODE == 'CL ') & (amt2 != 'c-1h') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_mix(self):
        rules = [
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE != 'VE ') & (SNDR_CNTRY_CODE == 'CL ') & (SUB_FLOW == 'MS Send Money Internal') & (amt2 != 'a-1k') & (SELLER_SEG == '04 YS') & (RCVR_CNTRY_CODE != 'PE ') & (RCVR_CNTRY_CODE != 'VE ') & (dof_bin != 'c-90')",
            "(dof_bin != 'e->1y') & (SNDR_CNTRY_CODE == 'VE ') & (amt2 != 'b-5h') & (SELLER_SEG == '04 YS') & (RCVR_CNTRY_CODE != 'MX ') & (RCVR_CNTRY_CODE != 'CO ') & (RCVR_CNTRY_CODE == 'CL ')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _duplicate_rows_to_new_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_latam_1_3_real'
        dest_db = "pp_scratch_risk"
        weight_a = 312
        weight_b = 140
        weight_c = 11
        weight_d = 11
        weight_e = 1
        dest_table = "ms_auto_trend_latam_1_3_real_{}_{}_{}_{}_{}".format(weight_a, weight_b, weight_c, weight_d, weight_e)
        instance.duplicate_rows_to_new_table(src_db, src_table, dest_db, dest_table, weight_a, weight_b, weight_c, weight_d, weight_e)

    def _duplicate_rows_from_bad_and_sample_from_good_into_new_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_latam'
        dest_db = "pp_scratch_risk"
        bad_scale = 1
        good_scale = 3

        # weight_a = 28
        # weight_b = 15
        # weight_c = 19
        # weight_d = 13
        # weight_e = 25
        weight_a = 7
        weight_b = 4
        weight_c = 5
        weight_d = 3
        weight_e = 6
        dest_table = "ms_auto_trend_latam_{}_{}__{}_{}_{}_{}_{}_v2".format(bad_scale, good_scale, weight_a, weight_b, weight_c, weight_d, weight_e)
        instance.duplicate_rows_from_bad_and_sample_from_good_into_new_table(src_db, src_table, dest_db, dest_table,
                                                                             bad_scale, good_scale,
                                                                             weight_a, weight_b, weight_c, weight_d, weight_e)

    def _generate_hl_job_json(self):
        #	pp_scratch_risk.ms_auto_trend_latam_off_ebay_ep_consumer_train pp_scratch_risk.ms_auto_trend_latam_off_ebay_ep_consumer_train
        training_table = "ms_auto_trend_latam_off_ebay_ep_consumer_train"
        testing_table = "ms_auto_trend_latam_off_ebay_ep_consumer_test"
        instance.generate_hl_job_json(training_table, testing_table)

    def _add_weight_col_to_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_latam_1_3'
        # weight_a = 0.312
        # weight_b = 0.140
        # weight_c = 0.011
        # weight_d = 0.011
        # weight_e = 0.001
        weight_a = 10 * 46
        weight_b = 8 * 27
        weight_c = 4.6 * 5
        weight_d = 3.7 * 5
        weight_e = 1 * 1
        instance.add_weight_col_to_table(src_db, src_table, weight_a, weight_b, weight_c, weight_d, weight_e)

    def _update_weight_col_in_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_latam_1_3'
        src_col = 'PMT_USD_AMT'
        instance.update_weight_col_in_table(src_db, src_table, src_col)

    def _update_custom_weight_col_in_table(self):
        src_db = "pp_scratch_risk"
        src_table = 'ms_auto_trend_latam_1_3'
        src_col = 'PMT_USD_AMT'
        instance.update_custom_weight_col_in_table(src_db, src_table, src_col)