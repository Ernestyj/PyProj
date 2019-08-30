# -*- coding: utf-8 -*-
import os
import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import pandas as pd
import traceback
import logging

from tools.settings import *
from tools.utility import datetime2str


MYSQL_CONF = PROJECT_CONFIG['mysql_rule360_alert']


class MysqlQueryBase():
    def __init__(self):
        self.mysql_con = None
        self.sqlalchemy_con = None

    def _init_mysql_connection(self):
        self.mysql_con = MySQLdb.connect(host=MYSQL_CONF['host'],  # your host, usually localhost
                                   user=MYSQL_CONF['username'],  # your username
                                   passwd=MYSQL_CONF['password'],  # your password
                                   db=MYSQL_CONF['defaultdb'])  # name of the data base

    def _init_sqlalchemy_mysql_connection(self, defaultDB=None):
        db = defaultDB if defaultDB is not None else MYSQL_CONF['defaultdb']
        self.sqlalchemy_con = create_engine('mysql://{}:{}@{}/{}'.format(MYSQL_CONF['username'],
                                                                  MYSQL_CONF['password'],
                                                                  MYSQL_CONF['host'],
                                                                  db))

    def _close_all_mysql_connection(self):
        if self.mysql_con is not None:
            self.mysql_con.close()
        if self.sqlalchemy_con is not None:
            self.sqlalchemy_con.dispose()

    def query_sample(self):
        self._init_mysql_connection()
        sql = """
        SELECT '1';
        """
        df = pd.read_sql(sql=sql, con=self.mysql_con)
        self._close_all_mysql_connection()
        return df

    def query(self, queryString, logString=''):
        logger_.debug('[mysql] Start  query {}, sql=\n{}'.format(logString, queryString))
        self._init_mysql_connection()
        try:
            df = pd.read_sql(sql=queryString, con=self.mysql_con)
            logger_.debug('[mysql] Finish  query {}, len(df)={}'.format(logString, len(df)))
            self._close_all_mysql_connection()
            return df
        except Exception as e:
            traceback.print_exc()
            logger_.error("[mysql] Exception in query {}, e.message={}".format(logString, e.message))
            self.mysql_con.rollback()
            self._close_all_mysql_connection()
            return None

    def execute(self, sqlString, logString='', muteLog=False):
        if not muteLog:
            logger_.debug('[mysql] Start  execute {}, sql=\n{}'.format(logString, sqlString))
        self._init_mysql_connection()
        try:
            cursor = self.mysql_con.cursor()
            result = cursor.execute(sqlString)
            self.mysql_con.commit()
            if not muteLog:
                logger_.debug('[mysql] Finish  execute {}, result={}'.format(logString, result))
            self._close_all_mysql_connection()
            return True
        except Exception as e:
            traceback.print_exc()
            logger_.error("[mysql] Exception in execute {}, e.message={}".format(logString, e.message))
            self.mysql_con.rollback()
            self._close_all_mysql_connection()
            return False

    def updateByID(self, table, col_id, val_id, col_update_ts, **update_params):
        setList = []
        for key, value in update_params.iteritems():
            setList.append(' {}="{}" '.format(key, value))
        sql = '''
        update {table} set {col_update_ts}='{now_ts}', {set_vals} where {col_id}='{val_id}'
        '''.format(table=table, col_update_ts=col_update_ts, now_ts=datetime2str(datetime.now(tz=TIMEZONE)), set_vals=','.join(setList), col_id=col_id, val_id=val_id)
        logger_.debug('[mysql] Start  update {}, sql=\n{}'.format(table, sql))
        self._init_mysql_connection()
        try:
            cursor = self.mysql_con.cursor()
            result = cursor.execute(sql)
            self.mysql_con.commit()
            logger_.debug('[mysql] Finish  update {}, result={}'.format(table, result))
            self._close_all_mysql_connection()
            return True
        except Exception as e:
            traceback.print_exc()
            logger_.error("[mysql] Exception in update {}, e.message={}".format(table, e.message))
            self.mysql_con.rollback()
            self._close_all_mysql_connection()
            return False
        pass

    def insertDF(self, df, tableName, dbName=None, logString=''):
        logger_.debug('[mysql] Start  insert df into {}.{}, {}'.format(dbName, tableName, logString))
        self._init_sqlalchemy_mysql_connection(dbName)
        try:
            df.to_sql(name=tableName, con=self.sqlalchemy_con, if_exists='append', index=False)
            self._close_all_mysql_connection()
            return df
        except IntegrityError as e:
            traceback.print_exc()
            self._close_all_mysql_connection()
            logger_.error('[mysql] IntegrityError in insert df into {}.{}, e={}'.format(dbName, tableName, e))
        except Exception as e:
            traceback.print_exc()
            self._close_all_mysql_connection()
            logger_.error("[mysql] Exception in insert df into {}.{}, e={}".format(dbName, tableName, e))


# singleton
mysql_query_instance = MysqlQueryBase()
