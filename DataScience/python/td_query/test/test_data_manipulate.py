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

    def _transalte_100_63_22_14_1(self):
        rules = [
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C')",
            "(SELLER_CONSUMER_SEG == 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string == '10008') & (amt2 != 'c-1h') & (amt2 != 'e-<50')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_30_20_3_4_1(self):
        rules = [
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 == 'a-1k') & (SUB_FLOW != 'MS Money Request - Invoicing') & (SUB_FLOW == 'MS Mobile Cons App Send Money - Commercial') & (IS_ULP_TRANS_T_F >= 0.5)",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 == 'a-1k') & (SUB_FLOW != 'MS Money Request - Invoicing') & (SUB_FLOW == 'MS Mobile Cons App Send Money - Commercial') & (IS_ULP_TRANS_T_F < 0.5)",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 == 'a-1k') & (SUB_FLOW != 'MS Money Request - Invoicing') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_30_20_3_4_1_nloss(self):
        rules = [
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string == '10008') & (SUB_FLOW == 'MS Mobile Cons App Send Money - Commercial') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C') & (SELLER_SEG == '04 YS')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string != '10008') & (amt2 != 'e-<50') & (dc_string != '10002') & (amt2 != 'd-50') & (SUB_FLOW != 'MS Mobile Money Request - Invoicing') & (SUB_FLOW != 'MS Money Request') & (SUB_FLOW != 'MS Mobile Money Request') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'c-1h') & (dc_string == '10010')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string == '10008') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial') & (SELLER_CONSUMER_SEG == 'C') & (amt2 != 'c-1h') & (amt2 != 'd-50') & (amt2 != 'e-<50')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '10008') & (dc_string != '<missing>') & (amt2 == 'a-1k') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial') & (SUB_FLOW == 'MS Send Money Internal') & (dc_string == '10002')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 == 'a-1k') & (SUB_FLOW != 'MS Money Request - Invoicing') & (SUB_FLOW == 'MS Mobile Cons App Send Money - Commercial') & (IS_ULP_TRANS_T_F >= 0.5)",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string != '10008') & (amt2 != 'e-<50') & (dc_string != '10002') & (amt2 != 'd-50') & (SUB_FLOW != 'MS Mobile Money Request - Invoicing') & (SUB_FLOW != 'MS Money Request') & (SUB_FLOW != 'MS Mobile Money Request') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'c-1h') & (dc_string != '10010') & (SUB_FLOW == 'MS Send Money Internal') & (amt2 != 'a-1k') & (RCVR_CNTRY_CODE != 'CA ') & (SELLER_SEG != '04 YS')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '10008') & (dc_string != '<missing>') & (amt2 == 'a-1k') & (SUB_FLOW == 'MS Mobile Cons App Send Money - Commercial')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 != 'a-1k') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 == 'b-5h')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string == '10008') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial') & (SELLER_CONSUMER_SEG != 'C') & (SUB_FLOW == 'MS Send Money Internal') & (amt2 == 'a-1k')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '10008') & (dc_string != '<missing>') & (amt2 == 'a-1k') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial') & (SUB_FLOW == 'MS Send Money Internal') & (dc_string != '10002') & (SELLER_SEG == '04 YS') & (dc_string == '10010')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 == 'a-1k') & (SUB_FLOW != 'MS Money Request - Invoicing') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '10008') & (dc_string != '<missing>') & (amt2 == 'a-1k') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial') & (SUB_FLOW == 'MS Send Money Internal') & (dc_string != '10002') & (SELLER_SEG == '04 YS') & (dc_string != '10010')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string != '10008') & (amt2 != 'e-<50') & (dc_string != '10002') & (amt2 != 'd-50') & (SUB_FLOW != 'MS Mobile Money Request - Invoicing') & (SUB_FLOW != 'MS Money Request') & (SUB_FLOW != 'MS Mobile Money Request') & (IS_ULP_TRANS_T_F < 0.5) & (amt2 != 'c-1h') & (dc_string == '10003')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 == 'a-1k') & (SUB_FLOW != 'MS Money Request - Invoicing') & (SUB_FLOW == 'MS Mobile Cons App Send Money - Commercial') & (IS_ULP_TRANS_T_F < 0.5)",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string != '10008') & (amt2 != 'e-<50') & (dc_string == '10002') & (amt2 == 'a-1k')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 == 'a-1k') & (SUB_FLOW == 'MS Money Request - Invoicing')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string != '10008') & (amt2 != 'e-<50') & (dc_string != '10002') & (amt2 != 'd-50') & (SUB_FLOW == 'MS Mobile Money Request - Invoicing') & (amt2 != 'c-1h') & (RCVR_CNTRY_CODE != 'CA ') & (dc_string != '<missing>') & (amt2 == 'a-1k')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string != '10008') & (amt2 != 'e-<50') & (dc_string != '10002') & (amt2 != 'd-50') & (SUB_FLOW != 'MS Mobile Money Request - Invoicing') & (SUB_FLOW != 'MS Money Request') & (SUB_FLOW != 'MS Mobile Money Request') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'c-1h') & (dc_string != '10010') & (SUB_FLOW == 'MS Send Money Internal') & (amt2 == 'a-1k') & (RCVR_CNTRY_CODE != 'CA ') & (dc_string != '<missing>')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_164_89_5_8_1(self):
        rules = [
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (dc_string != '10005') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C') & (SELLER_SEG == '04 YS')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (dc_string != '10005') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C') & (SELLER_SEG != '04 YS')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'c-1h') & (amt2 != 'e-<50')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_1000_500_100_50_1(self):
        rules = [
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 != 'c-1h') & (dc_string != '10005') & (amt2 != 'd-50') & (dc_string != '12123') & (SELLER_CONSUMER_SEG == 'C') & (amt2 == 'a-1k') & (SELLER_SEG == '04 YS') & (dc_string == '10008') & (SUB_FLOW == 'MS Send Money Internal')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 != 'c-1h') & (dc_string != '10005') & (amt2 != 'd-50') & (dc_string != '12123') & (SELLER_CONSUMER_SEG == 'C') & (amt2 == 'a-1k') & (SELLER_SEG == '04 YS') & (dc_string == '10008') & (SUB_FLOW != 'MS Send Money Internal')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 == 'a-1k') & (SUB_FLOW != 'MS Money Request - Invoicing') & (SUB_FLOW == 'MS Mobile Cons App Send Money - Commercial') & (IS_ULP_TRANS_T_F >= 0.5)",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 != 'c-1h') & (dc_string != '10005') & (amt2 != 'd-50') & (dc_string != '12123') & (SELLER_CONSUMER_SEG == 'C') & (amt2 == 'a-1k') & (SELLER_SEG != '04 YS')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 != 'c-1h') & (dc_string != '10005') & (amt2 != 'd-50') & (dc_string != '12123') & (SELLER_CONSUMER_SEG == 'C') & (amt2 == 'a-1k') & (SELLER_SEG == '04 YS') & (dc_string != '10008')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 == 'a-1k') & (SUB_FLOW != 'MS Money Request - Invoicing') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_1_1_1_1_1(self):
        rules = [
            "(SELLER_CONSUMER_SEG != 'Y') & (SELLER_SEG == '04 YS') & (amt2 != 'e-<50') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 != 'd-50')",
            "(SELLER_CONSUMER_SEG == 'Y') & (SELLER_SEG == '04 YS') & (amt2 != 'e-<50') & (SUB_FLOW == 'MS Send Money Internal') & (IS_ULP_TRANS_T_F >= 0.5) & (RCVR_CNTRY_CODE != 'CA ') & (dc_string == '10008')",
            "(SELLER_CONSUMER_SEG != 'Y') & (SELLER_SEG != '04 YS') & (amt2 != 'e-<50') & (SUB_FLOW != 'MS Mobile Cons App Send Money - Commercial') & (amt2 == 'a-1k') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>')",
            "(SELLER_CONSUMER_SEG == 'Y') & (SELLER_SEG != '04 YS') & (SUB_FLOW != 'MS Send Money Internal') & (SUB_FLOW == 'MS Mobile Money Request - Invoicing API')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_mix(self):
        rules = [
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (dc_string != '10005') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C') & (SELLER_SEG == '04 YS') & (dc_string == '10008') & (SUB_FLOW == 'MS Send Money Internal')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (dc_string != '10005') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C') & (SELLER_SEG == '04 YS') & (dc_string == '10008') & (SUB_FLOW != 'MS Send Money Internal')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (dc_string != '10005') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C') & (SELLER_SEG != '04 YS')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (dc_string != '10005') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C') & (SELLER_SEG == '04 YS') & (dc_string != '10008')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (IS_ULP_TRANS_T_F >= 0.5) & (amt2 != 'c-1h') & (amt2 != 'e-<50')",
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_tpv(self):
        rules = [
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C') & (SELLER_SEG == '04 YS') & (SUB_FLOW == 'MS Send Money Internal') & (dc_string == '10008')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C') & (SELLER_SEG == '04 YS') & (SUB_FLOW != 'MS Send Money Internal')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string != '10008') & (SUB_FLOW != 'MS Mobile Money Request') & (SUB_FLOW != 'MS Money Request') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string == '10002') & (amt2 != 'c-1h')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string != '10008') & (SUB_FLOW != 'MS Mobile Money Request') & (SUB_FLOW != 'MS Money Request') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '10002') & (amt2 != 'c-1h') & (SUB_FLOW == 'MS Send Money Internal') & (RCVR_CNTRY_CODE != 'CA ') & (dc_string != '12122') & (dc_string != '10010') & (SELLER_SEG != '04 YS') & (amt2 != 'e-<50')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 == 'a-1k') & (SELLER_CONSUMER_SEG == 'C') & (SELLER_SEG != '04 YS')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 == 'a-1k') & (IS_ULP_TRANS_T_F >= 0.5)"
        ]
        result = instance.translate_hyperloop_rules_to_sql(rules)
        print(result)

    def _transalte_tpv2(self):
        rules = [
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 != 'c-1h') & (dc_string != '10005') & (amt2 != 'd-50') & (amt2 != 'e-<50') & (SELLER_CONSUMER_SEG == 'C') & (dc_string != '12123') & (amt2 == 'a-1k') & (SELLER_SEG == '04 YS') & (SUB_FLOW == 'MS Send Money Internal') & (dc_string == '10008')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 != 'c-1h') & (dc_string != '10005') & (amt2 != 'd-50') & (amt2 != 'e-<50') & (SELLER_CONSUMER_SEG == 'C') & (dc_string != '12123') & (amt2 == 'a-1k') & (SELLER_SEG == '04 YS') & (SUB_FLOW != 'MS Send Money Internal')",
            "(SELLER_CONSUMER_SEG != 'Y') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '<missing>') & (amt2 != 'c-1h') & (dc_string != '10005') & (amt2 != 'd-50') & (amt2 != 'e-<50') & (SELLER_CONSUMER_SEG == 'C') & (dc_string != '12123') & (amt2 == 'a-1k') & (SELLER_SEG != '04 YS')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string != '10008') & (SUB_FLOW != 'MS Mobile Money Request') & (SUB_FLOW != 'MS Money Request') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string == '10002') & (amt2 != 'c-1h')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string != '10008') & (SUB_FLOW != 'MS Mobile Money Request') & (SUB_FLOW != 'MS Money Request') & (IS_ULP_TRANS_T_F >= 0.5) & (dc_string != '10002') & (amt2 != 'c-1h') & (SUB_FLOW == 'MS Send Money Internal') & (RCVR_CNTRY_CODE != 'CA ') & (dc_string != '12122') & (dc_string != '10010') & (SELLER_SEG != '04 YS') & (amt2 != 'e-<50')",
            "(SELLER_CONSUMER_SEG == 'Y') & (dc_string == '10008') & (amt2 == 'a-1k') & (IS_ULP_TRANS_T_F >= 0.5)"
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