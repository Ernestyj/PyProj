# -*- coding: utf-8 -*-
import os
import pandas as pd
from teradata.api import DatabaseError
import pickle

from td_query.td_query_base import *
from td_query import ROOT_PATH


class DataManipulate(TeradataQueryBase):
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

    def duplicate_rows_to_new_table(self, src_db="pp_scratch_risk", src_table='ms_auto_trend_us2_1_3',
                                    dest_db="pp_scratch_risk", dest_table="ms_auto_trend_us2_1_3_100_100_1_1_1",
                                    weight_a=1, weight_b=1, weight_c=1, weight_d=1, weight_e=1, ):
        # get df from src table
        df = self.query(query_string='''select * from {}.{};'''.format(src_db, src_table))
        with open(ROOT_PATH + '/external/df_{}.pickle'.format(src_table), 'wb') as f: # save
            pickle.dump(df, f)
        self.logger.info('Finish saving df table "{}"'.format(src_table))
        # drop dest table, if exist
        self.drop_table(dest_db, dest_table)
        # create from src table with data
        self.create_table_from_src_table_with_data(src_db, src_table, dest_db, dest_table)
        # duplicate according to weight
        df_a = df[df['amt2'] == 'a-1k']
        df_b = df[df['amt2'] == 'b-5h']
        df_c = df[df['amt2'] == 'c-1h']
        df_d = df[df['amt2'] == 'd-50']
        df_e = df[df['amt2'] == 'e-<50']
        # insert rows into dest table
        if weight_a - 1 > 0:
            self.insert_to_table(pd.concat([df_a]*(weight_a-1), ignore_index=True), dest_db, dest_table)
        if weight_b - 1 > 0:
            self.insert_to_table(pd.concat([df_b]*(weight_b-1), ignore_index=True), dest_db, dest_table)
        if weight_c - 1 > 0:
            self.insert_to_table(pd.concat([df_c]*(weight_c-1), ignore_index=True), dest_db, dest_table)
        if weight_d - 1 > 0:
            self.insert_to_table(pd.concat([df_d]*(weight_d-1), ignore_index=True), dest_db, dest_table)
        if weight_e - 1 > 0:
            self.insert_to_table(pd.concat([df_e]*(weight_e-1), ignore_index=True), dest_db, dest_table)


# singleton
data_manipulate_instance = DataManipulate()