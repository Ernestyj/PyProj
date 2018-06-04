# -*- coding: utf-8 -*-
import os
import MySQLdb
import pandas as pd
import traceback
import logging

from mysql_query import ROOT_PATH
from tools.json_tools import JsonConf


class TDJobTimeUsedQuery():
    def __init__(self, conf_path=os.path.join(ROOT_PATH, 'conf/conf.json')):
        # init param
        self.conf_path = conf_path
        # init param placeholder
        self.logger = None
        self.conf = None
        self.conf_mysql = None
        self.con = None
        self.df_time_used = None

    def init(self):
        self._init_logger()
        self._get_conf()
        self._init_connect_mysql()

    def query(self):
        sql = """
        SELECT * FROM td_refresh_job_time_used WHERE job_start_time BETWEEN NOW() - INTERVAL 30 DAY AND NOW();
        """
        self.df_time_used = pd.read_sql(sql=sql, con=self.con)
        return self.df_time_used

    # init helper##############################################################################
    def _init_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] : %(message)s'))
        self.logger.addHandler(consoleHandler)

    def _get_conf(self):
        try:
            self.conf = JsonConf().get_json_conf(path=self.conf_path)
            self.conf_mysql = self.conf['mysql']
        except Exception as e:
            traceback.print_exc()
            self.logger.error(e.message)

    def _init_connect_mysql(self):
        mysql_conf = self.conf_mysql
        self.con = MySQLdb.connect(host=mysql_conf['host'],  # your host, usually localhost
                                     user=mysql_conf['username'],  # your username
                                     passwd=mysql_conf['password'],  # your password
                                     db=mysql_conf['defaultdb'])  # name of the data base

# singleton
job_time_used_query_instance = TDJobTimeUsedQuery()