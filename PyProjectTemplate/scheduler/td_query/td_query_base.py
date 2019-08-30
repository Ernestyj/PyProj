# -*- coding: utf-8 -*-
import logging
import os
import traceback
import pandas as pd
from teradata.api import DatabaseError

from tools import Teradata, TeradataOdbc
from tools.settings import *


TD_CONFIG = PROJECT_CONFIG['teradata']


class TDQueryBase():
    def __init__(self):
        self.td_con = None

    def _init_teradata_connection(self, td_platform='SIMBA', is_service_account=True): # JACKAL or SIMBA
        host = TD_CONFIG[td_platform]
        user_name = TD_CONFIG['username']
        password = TD_CONFIG['password']
        if td_platform == 'SIMBA' and is_service_account:
            user_name = TD_CONFIG['username_simba']
            password = TD_CONFIG['password_simba']
        # elif td_platform == 'JACKAL' and is_service_account:
        #     user_name = TD_CONFIG['username_jackal']
        #     password = TD_CONFIG['password_jackal']
        if IS_DEPLOY: # deploy mode should use odbc
            self.td_con = TeradataOdbc(host=host, user_name=user_name, password=password)
        else:
            self.td_con = Teradata(host=host, user_name=user_name, password=password)

    def query_td_sample(self):
        self._init_teradata_connection()
        return self.td_con.query(query_string='''select * from pp_oap_sing_jyang2_t.test;''')

    def query(self, queryString=None, logString='', tdPlatform='SIMBA', is_service_account=True):
        logger_.debug('[TD] Start  query {}, sql=\n{}'.format(logString, queryString))
        self._init_teradata_connection(td_platform=tdPlatform, is_service_account=is_service_account)
        try:
            df = self.td_con.query(queryString)
            df.columns = [column.lower() for column in df.columns]  # odbc teradata returns upper case column names
            logger_.debug('[TD] Finish  query {}, len(df)={}'.format(logString, len(df)))
            return df
        except Exception as e:
            traceback.print_exc()
            logger_.error("[TD] Exception in query {}, e.message={}".format(logString, e.message))
            return None

    def execute(self, sqlString=None, logString='', tdPlatform='SIMBA', is_service_account=True):
        logger_.debug('[TD] Start  execute {}, sql=\n{}'.format(logString, sqlString))
        self._init_teradata_connection(td_platform=tdPlatform, is_service_account=is_service_account)
        try:
            result = self.td_con.execute(sqlString)
            logger_.debug('[TD] Finish  execute {}, result={}'.format(logString, result))
            return True
        except Exception as e:
            traceback.print_exc()
            logger_.error("[TD] Exception in execute {}, e.message={}".format(logString, e.message))
            return False

    def dropTable(self, dbTableName, logString='', tdPlatform='SIMBA', is_service_account=True):
        logger_.debug('[TD] Start  drop {}, {}'.format(dbTableName, logString))
        self._init_teradata_connection(td_platform=tdPlatform, is_service_account=is_service_account)
        try:
            self.td_con.execute('''drop table {}'''.format(dbTableName))
            return True
        except DatabaseError as e:
            logger_.debug("[TD] DatabaseError in drop {}, e={}".format(dbTableName, e))
            return False
        except Exception as e:
            logger_.debug("[TD] Exception in drop {}, e={}".format(dbTableName, e))
            return False


# singleton
td_query_instance = TDQueryBase()