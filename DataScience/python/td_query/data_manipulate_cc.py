# -*- coding: utf-8 -*-
import os
import pandas as pd
from teradata.api import DatabaseError
import pickle

from td_query.td_query_base import *
from td_query import ROOT_PATH


class DataManipulateCC(TeradataQueryBase):
    def __init__(self, conf_path=os.path.join(ROOT_PATH, 'conf/conf.json'), teradata_platform='JACKAL'):
        # super.__init__(conf_path, teradata_platform)
        TeradataQueryBase.__init__(self, conf_path, teradata_platform)

    def query(self, query_string):
        self.logger.info('Start  querying, query="{}"'.format(query_string))
        df = self.teradata.query(query_string=query_string)
        self.logger.info('Finish querying, query="{}"'.format(query_string))
        return df

    def query_table_top_rows(self, table):
        self.logger.info('Start  querying table "{}" top rows'.format(table))
        return self.teradata.query(query_string='''select top 10 * from {};'''.format(table))

    def insert_to_table(self, df, database="pp_scratch_risk", table="ms_auto_trend_us2_1_3"):
        def approximate_chunk_size(df):
            if len(df) > 0:
                return int(1e6 / (sum(df.memory_usage()) / len(df)) / 4)
            else:
                return 0

        chunk_size = approximate_chunk_size(df) # get chunk size, or insert to teradata will exceed 1M limit
        self.logger.info('Start  inserting dataframe into table "{}", chunk_size={}'.format(table, chunk_size))
        self.teradata.upsert(data_frame=df, database=database, table=table, chunk_size=chunk_size, batch=True)
        self.logger.info('Finish inserting dataframe into table "{}"'.format(table))

    def create_table_from_src_table_schema(self, src_db="pp_scratch_risk", src_table='ms_auto_trend_us2_1_3',
                                           dest_db="pp_scratch_risk", dest_table="ms_auto_trend_us2_1_3_100_100_1_1_1"):
        self.logger.info('Start  creating table "{}" from table "{}" with no data'.format(dest_table, src_table))
        self.teradata.execute('''CREATE multiset TABLE {}.{} AS {}.{} WITH NO DATA;'''.format(dest_db, dest_table, src_db, src_table))
        self.logger.info('Finish creating table "{}" from table "{}" with no data'.format(dest_table, src_table))

    def create_table_from_src_table_with_data(self, src_db="pp_scratch_risk", src_table='ms_auto_trend_us2_1_3',
                                           dest_db="pp_scratch_risk", dest_table="ms_auto_trend_us2_1_3_100_100_1_1_1"):
        self.logger.info('Start  creating table "{}" from table "{}" with data'.format(dest_table, src_table))
        self.teradata.execute('''CREATE multiset TABLE {}.{} AS {}.{} WITH DATA;'''.format(dest_db, dest_table, src_db, src_table))
        self.logger.info('Finish creating table "{}" from table "{}" with data'.format(dest_table, src_table))

    def drop_table(self, database="pp_scratch_risk", table="ms_auto_trend_us2_1_3"):
        self.logger.info('Start  dropping table "{}"'.format(table))
        try:
            self.teradata.execute('''drop table {}.{}'''.format(database, table))
            self.logger.info('Finish dropping table "{}"'.format(table))
        except DatabaseError as e:
            self.logger.error("DatabaseError occurred, error={}".format(e))
        except Exception as e:
            self.logger.error("Exception occurred, error={}".format(e))

    # def duplicate_rows_to_new_table(self, src_db="pp_scratch_risk", src_table='ms_auto_trend_us2_1_3',
    #                                 dest_db="pp_scratch_risk", dest_table="ms_auto_trend_us2_1_3_100_100_1_1_1",
    #                                 weight_a=1, weight_b=1, weight_c=1, weight_d=1, weight_e=1, ):
    #     # get df from src table
    #     df = self.query(query_string='''select * from {}.{};'''.format(src_db, src_table))
    #     with open(ROOT_PATH + '/external/df_{}.pickle'.format(src_table), 'wb') as f: # save
    #         pickle.dump(df, f)
    #     self.logger.info('Finish saving df table "{}"'.format(src_table))
    #     # drop dest table, if exist
    #     self.drop_table(dest_db, dest_table)
    #     # create from src table with data
    #     self.create_table_from_src_table_with_data(src_db, src_table, dest_db, dest_table)
    #     # duplicate according to weight
    #     df_a = df[df['AMT2'] == 'a-1k']
    #     df_b = df[df['AMT2'] == 'b-5h']
    #     df_c = df[df['AMT2'] == 'c-1h']
    #     df_d = df[df['AMT2'] == 'd-50']
    #     df_e = df[df['AMT2'] == 'e-<50']
    #     # insert rows into dest table
    #     if weight_a - 1 > 0:
    #         self.insert_to_table(pd.concat([df_a]*(weight_a-1), ignore_index=True), dest_db, dest_table)
    #     if weight_b - 1 > 0:
    #         self.insert_to_table(pd.concat([df_b]*(weight_b-1), ignore_index=True), dest_db, dest_table)
    #     if weight_c - 1 > 0:
    #         self.insert_to_table(pd.concat([df_c]*(weight_c-1), ignore_index=True), dest_db, dest_table)
    #     if weight_d - 1 > 0:
    #         self.insert_to_table(pd.concat([df_d]*(weight_d-1), ignore_index=True), dest_db, dest_table)
    #     if weight_e - 1 > 0:
    #         self.insert_to_table(pd.concat([df_e]*(weight_e-1), ignore_index=True), dest_db, dest_table)

    def get_all_bad_and_sample_from_good_into_new_table(self, src_db="pp_scratch_risk",
                                                                    src_table='ms_auto_trend_apac',
                                                                    dest_db="pp_scratch_risk",
                                                                    dest_table="ms_auto_trend_apac_1_3_100_100_1_1_1",
                                                                    bad_scale=1, good_scale=3,
                                                                    weight_a=1, weight_b=1, weight_c=1, weight_d=1, weight_e=1, ):
        temp_bad_table = "temp_bad_" + dest_table
        # drop temp bad table, if exist
        self.drop_table(dest_db, temp_bad_table)
        # create good sample table from src table
        self.teradata.execute('''
        CREATE TABLE {}.{} AS
        (
        SELECT * FROM {}.{} where brm_bad_tag_assigned in ('3_STOLEN_CC_CB','4_UNAUTH_RESTR')
        ) WITH DATA;
        '''.format(dest_db, temp_bad_table, src_db, src_table))
        self.logger.info('Finish creating all bad table "{}" from table "{}"'.format(temp_bad_table, src_table, ))

        # select count from current dest table (only bad)
        count_df = self.query(query_string='''select count(*) from {}.{}'''.format(dest_db, temp_bad_table))
        bad_count = float(count_df.iloc[0, 0])
        self.logger.info('total bad (include copied) count={}'.format(bad_count))
        # select good count from src table (only good)
        count_df = self.query(query_string='''select count(*) from {}.{} where brm_bad_tag_assigned not in ('3_STOLEN_CC_CB','4_UNAUTH_RESTR');'''.format(src_db, src_table))
        good_count = float(count_df.iloc[0, 0])
        self.logger.info('total good (has_gloss = 0) count={}'.format(good_count))
        # cal good sample rate
        good_sample_rate = bad_count * 1.0 / bad_scale * good_scale / good_count
        self.logger.info('bad_scale={}, good_scale={}, good_sample_rate={}'.format(bad_scale, good_scale, good_sample_rate))

        temp_good_table = "temp_good_sample_" + dest_table
        # drop temp good sample table, if exist
        self.drop_table(dest_db, temp_good_table)
        # create good sample table from src table
        self.teradata.execute('''
        CREATE TABLE {}.{} AS
        (
        SELECT * FROM {}.{} where brm_bad_tag_assigned not in ('3_STOLEN_CC_CB','4_UNAUTH_RESTR') SAMPLE {}
        ) WITH DATA;
        '''.format(dest_db, temp_good_table, src_db, src_table, good_sample_rate))
        self.logger.info('Finish creating table "{}" from table "{}" with good_sample_rate={}'.format(temp_good_table, src_table, good_sample_rate))

        # drop dest table, if exist
        self.drop_table(dest_db, dest_table)
        # union dest table with good src table (in sample rate)
        self.logger.info('Start  union table "{}" and table "{}" into new table "{}"'.format(temp_bad_table, temp_good_table, dest_table))
        self.teradata.execute('''
        CREATE multiset TABLE {}.{} AS
        (
        SELECT * FROM {}.{}
        UNION
        SELECT * FROM {}.{}
        ) WITH DATA;
        '''.format(dest_db, dest_table, dest_db, temp_bad_table, dest_db, temp_good_table))
        self.logger.info('Finish union table "{}" and table "{}" into new table "{}"'.format(temp_bad_table, temp_good_table, dest_table))

        # get df from src bad table TODO
        # df = self.query(query_string='''select * from {}.{};'''.format(dest_db, dest_table))
        # df.fillna(0)

        # clear temp bad table
        self.drop_table(dest_db, temp_bad_table)
        self.drop_table(dest_db, temp_good_table)
        self.logger.info('Finish all, with new table "{}"'.format(dest_table))

    def get_all_bad_and_sample_from_good_into_new_table_reverse(self, src_db="pp_scratch_risk",
                                                                    src_table='ms_auto_trend_apac',
                                                                    dest_db="pp_scratch_risk",
                                                                    dest_table="ms_auto_trend_apac_1_3_100_100_1_1_1",
                                                                    bad_scale=1, good_scale=3,
                                                                    weight_a=1, weight_b=1, weight_c=1, weight_d=1, weight_e=1, ):
        temp_bad_table = "temp_bad_" + dest_table
        # drop temp bad table, if exist
        self.drop_table(dest_db, temp_bad_table)
        # create good sample table from src table
        self.teradata.execute('''
        CREATE TABLE {}.{} AS
        (
        SELECT * FROM {}.{} where brm_bad_tag_assigned not in ('3_STOLEN_CC_CB','4_UNAUTH_RESTR')
        ) WITH DATA;
        '''.format(dest_db, temp_bad_table, src_db, src_table))
        self.logger.info('Finish creating all bad table "{}" from table "{}"'.format(temp_bad_table, src_table, ))

        # select count from current dest table (only bad)
        count_df = self.query(query_string='''select count(*) from {}.{}'''.format(dest_db, temp_bad_table))
        bad_count = float(count_df.iloc[0, 0])
        self.logger.info('total bad (include copied) count={}'.format(bad_count))
        # select good count from src table (only good)
        count_df = self.query(query_string='''select count(*) from {}.{} where brm_bad_tag_assigned in ('3_STOLEN_CC_CB','4_UNAUTH_RESTR');'''.format(src_db, src_table))
        good_count = float(count_df.iloc[0, 0])
        self.logger.info('total good (has_gloss = 0) count={}'.format(good_count))
        # cal good sample rate
        good_sample_rate = bad_count * 1.0 / bad_scale * good_scale / good_count
        self.logger.info('bad_scale={}, good_scale={}, good_sample_rate={}'.format(bad_scale, good_scale, good_sample_rate))

        temp_good_table = "temp_good_sample_" + dest_table
        # drop temp good sample table, if exist
        self.drop_table(dest_db, temp_good_table)
        # create good sample table from src table
        self.teradata.execute('''
        CREATE TABLE {}.{} AS
        (
        SELECT * FROM {}.{} where brm_bad_tag_assigned in ('3_STOLEN_CC_CB','4_UNAUTH_RESTR') SAMPLE {}
        ) WITH DATA;
        '''.format(dest_db, temp_good_table, src_db, src_table, good_sample_rate))
        self.logger.info('Finish creating table "{}" from table "{}" with good_sample_rate={}'.format(temp_good_table, src_table, good_sample_rate))

        # drop dest table, if exist
        self.drop_table(dest_db, dest_table)
        # union dest table with good src table (in sample rate)
        self.logger.info('Start  union table "{}" and table "{}" into new table "{}"'.format(temp_bad_table, temp_good_table, dest_table))
        self.teradata.execute('''
        CREATE multiset TABLE {}.{} AS
        (
        SELECT * FROM {}.{}
        UNION
        SELECT * FROM {}.{}
        ) WITH DATA;
        '''.format(dest_db, dest_table, dest_db, temp_bad_table, dest_db, temp_good_table))
        self.logger.info('Finish union table "{}" and table "{}" into new table "{}"'.format(temp_bad_table, temp_good_table, dest_table))

        # get df from src bad table TODO
        # df = self.query(query_string='''select * from {}.{};'''.format(dest_db, dest_table))
        # df.fillna(0)

        # clear temp bad table
        self.drop_table(dest_db, temp_bad_table)
        self.drop_table(dest_db, temp_good_table)
        self.logger.info('Finish all, with new table "{}"'.format(dest_table))

    def _translate_hyperloop_rule_to_sql(self, rule):
        mapping = {
            "(dc_string != '<missing>')": "(dc_card_type is not null)",
            "(amt2 == 'a-1k')": "(pmt_usd_amt > 1000)",
            "(amt2 == 'b-5h')": "(pmt_usd_amt > 500 and pmt_usd_amt <= 1000)",
            "(amt2 == 'c-1h')": "(pmt_usd_amt > 100 and pmt_usd_amt <= 500)",
            "(amt2 == 'd-50')": "(pmt_usd_amt > 50 and pmt_usd_amt <= 100)",
            "(amt2 == 'e-<50')": "(pmt_usd_amt <= 50)",

            "(amt2 != 'a-1k')": "(pmt_usd_amt <= 1000)", # pmt_usd_amt>1000
            "(amt2 != 'b-5h')": "(pmt_usd_amt > 1000 or pmt_usd_amt <= 500)", # pmt_usd_amt>500
            "(amt2 != 'c-1h')": "(pmt_usd_amt > 500 or pmt_usd_amt <= 100)",  # pmt_usd_amt>100
            "(amt2 != 'd-50')": "(pmt_usd_amt > 100 or pmt_usd_amt<=50)",   # pmt_usd_amt>50
            "(amt2 != 'e-<50')": "(pmt_usd_amt > 50)",  # pmt_usd_amt<=50

            "(dof_bin == 'a-7')": "(pmt_cre_dt-ACCT_CRE_DT <= 7)",
            "(dof_bin == 'b-30')": "(pmt_cre_dt-ACCT_CRE_DT > 7 and pmt_cre_dt-ACCT_CRE_DT <= 30)",
            "(dof_bin == 'c-90')": "(pmt_cre_dt-ACCT_CRE_DT > 30 and pmt_cre_dt-ACCT_CRE_DT <= 90)",
            "(dof_bin == 'd-1y')": "(pmt_cre_dt-ACCT_CRE_DT > 90 and pmt_cre_dt-ACCT_CRE_DT <= 365)",
            "(dof_bin == 'e->1y')":"(pmt_cre_dt-ACCT_CRE_DT > 365)",

            "(dof_bin != 'a-7')": "(pmt_cre_dt-ACCT_CRE_DT > 7)",
            "(dof_bin != 'b-30')": "(pmt_cre_dt-ACCT_CRE_DT <= 7 or pmt_cre_dt-ACCT_CRE_DT > 30)",
            "(dof_bin != 'c-90')": "(pmt_cre_dt-ACCT_CRE_DT <= 30 or pmt_cre_dt-ACCT_CRE_DT > 90)",
            "(dof_bin != 'd-1y')": "(pmt_cre_dt-ACCT_CRE_DT <= 90 or pmt_cre_dt-ACCT_CRE_DT > 365)",
            "(dof_bin != 'e->1y')":"(pmt_cre_dt-ACCT_CRE_DT <= 365)",

            "&": "and",
            "==": "=",
            "!=": "<>",
            "dc_string": "dc_card_type"
        }
        for k, v in mapping.items():
            if k in rule:
                rule = rule.replace(k, v)
        return rule

    def _combine_rules_sql(self, rule_sqls):
        result = "(" + rule_sqls[0] + ")"
        for i in range(1, len(rule_sqls)):
            result = " OR ".join([result, "(" + rule_sqls[i] + ")"])
        return result

    def translate_hyperloop_rules_to_sql(self, rules):
        rule_sqls = []
        for rule in rules:
            rule_sql = self._translate_hyperloop_rule_to_sql(rule)
            rule_sqls.append(rule_sql)
        result = self._combine_rules_sql(rule_sqls)
        return result

    def generate_hl_job_json(self, training_table, testing_table, template_name='hl_job_template.json'):
        json_str = ""
        with open(ROOT_PATH+'/external/{}'.format(template_name), 'r') as f:
            json_str = f.read()
        json_str = json_str.replace("training_table", training_table)
        json_str = json_str.replace("testing_table", testing_table)
        with open(ROOT_PATH+'/external/hl_job.json', 'w') as f:
            f.write(json_str)
        print("generated {} and {}".format(training_table, testing_table))

    # def add_weight_col_to_table(self, src_db="pp_scratch_risk", src_table='ms_auto_trend_us2_1_3',
    #                                 weight_a=1, weight_b=1, weight_c=1, weight_d=1, weight_e=1, ):
    #     try:
    #         # alter table add weight column in src table
    #         self.teradata.execute('''
    #         ALTER TABLE {}.{} ADD weight FLOAT DEFAULT 1.0;
    #         '''.format(src_db, src_table))
    #         self.logger.info('altered table "{}" add weight column with default value 1.0'.format(src_table, ))
    #     except DatabaseError as e:
    #         self.logger.error("DatabaseError occurred, error={}".format(e))
    #     except Exception as e:
    #         self.logger.error("Exception occurred, error={}".format(e))
    #
    #     # update weight column
    #     self.teradata.execute('''
    #     update {}.{} SET weight=(
    #     case
    #     when amt2='a-1k' then {}
    #     when amt2='b-5h' then {}
    #     when amt2='c-1h' then {}
    #     when amt2='d-50' then {}
    #     when amt2='e-<50' then {}
    #     end);
    #     '''.format(src_db, src_table, weight_a, weight_b, weight_c, weight_d, weight_e))
    #     self.logger.info('updated table "{}" weight column with {}, {}, {}, {}, {},'.format(src_table, weight_a, weight_b, weight_c, weight_d, weight_e))

    def update_weight_col_in_table(self, src_db="pp_scratch_risk", src_table='ms_auto_trend_us2_1_3', src_col='PP_MERCH_GROSS_LOSS'):
        try:
            # alter table add weight column in src table
            self.teradata.execute('''
            ALTER TABLE {}.{} ADD weight FLOAT DEFAULT 1.0;
            '''.format(src_db, src_table))
            self.logger.info('altered table "{}" add weight column with default value 1.0'.format(src_table, ))
        except DatabaseError as e:
            self.logger.error("DatabaseError occurred, error={}".format(e))
        except Exception as e:
            self.logger.error("Exception occurred, error={}".format(e))

        # update weight column
        self.teradata.execute('''
        update {}.{} SET weight={};
        update {}.{} SET weight=1 where weight is null;
        '''.format(src_db, src_table, src_col, src_db, src_table))
        self.logger.info('updated table "{}" weight column with column {}'.format(src_table, src_col))

    def update_custom_weight_col_in_table(self, src_db="pp_scratch_risk", src_table='ms_auto_trend_us2_1_3', src_col='PP_MERCH_GROSS_LOSS'):
        try:
            # alter table add weight column in src table
            self.teradata.execute('''
            ALTER TABLE {}.{} ADD weight FLOAT DEFAULT 1.0;
            '''.format(src_db, src_table))
            self.logger.info('altered table "{}" add weight column with default value 1.0'.format(src_table, ))
        except DatabaseError as e:
            self.logger.error("DatabaseError occurred, error={}".format(e))
        except Exception as e:
            self.logger.error("Exception occurred, error={}".format(e))

        # update weight column
        self.teradata.execute('''
        update {}.{} SET weight=(
        case 
        when usd_nLOSS_pp_amt is null or usd_nLOSS_pp_amt <= 0.0 then usd_amt 
        else usd_amt * 2
        end);
        update {}.{} SET weight=1 where weight is null;
        '''.format(src_db, src_table, src_db, src_table))
        self.logger.info('updated table "{}" weight column'.format(src_table, ))

    def add_is_cc_bad_col_in_table(self, src_db="pp_scratch_risk", src_table='ms_auto_trend_us2_1_3'):
        try:
            # alter table add is_cc_bad column in src table
            self.teradata.execute('''
            ALTER TABLE {}.{} ADD is_cc_bad BYTEINT DEFAULT 0;
            '''.format(src_db, src_table))
            self.logger.info('altered table "{}" add is_cc_bad column with default value 0'.format(src_table, ))
        except DatabaseError as e:
            self.logger.error("DatabaseError occurred, error={}".format(e))
        except Exception as e:
            self.logger.error("Exception occurred, error={}".format(e))

        # update is_cc_bad column
        self.teradata.execute('''
        update {}.{} SET is_cc_bad=(
        case 
        when brm_bad_tag_assigned in ('3_STOLEN_CC_CB', '4_UNAUTH_RESTR') then 1 
        else 0
        end);
        update {}.{} SET is_cc_bad=0 where is_cc_bad is null;
        '''.format(src_db, src_table, src_db, src_table))
        self.logger.info('updated table "{}" is_cc_bad column'.format(src_table, ))

    def add_is_cc_bad_reverse_col_in_table(self, src_db="pp_scratch_risk", src_table='ms_auto_trend_us2_1_3'):
        try:
            # alter table add is_cc_bad column in src table
            self.teradata.execute('''
            ALTER TABLE {}.{} ADD is_cc_bad BYTEINT DEFAULT 0;
            '''.format(src_db, src_table))
            self.logger.info('altered table "{}" add is_cc_bad column with default value 0'.format(src_table, ))
        except DatabaseError as e:
            self.logger.error("DatabaseError occurred, error={}".format(e))
        except Exception as e:
            self.logger.error("Exception occurred, error={}".format(e))

        # update is_cc_bad column
        self.teradata.execute('''
        update {}.{} SET is_cc_bad=(
        case 
        when brm_bad_tag_assigned in ('3_STOLEN_CC_CB', '4_UNAUTH_RESTR') then 0 
        else 1
        end);
        update {}.{} SET is_cc_bad=0 where is_cc_bad is null;
        '''.format(src_db, src_table, src_db, src_table))
        self.logger.info('updated table "{}" is_cc_bad column'.format(src_table, ))


# singleton
data_manipulate_cc_instance = DataManipulateCC()