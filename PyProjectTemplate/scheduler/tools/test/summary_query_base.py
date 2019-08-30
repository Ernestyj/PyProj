# -*- coding: utf-8 -*-
import logging
import traceback

from tools.td_tools import Teradata
from tools.td_odbc_tools import Teradata as TeradataOdbc


TD_CONFIG = {
    "username": "",
    "password": "",
    "JACKAL": "",
    "SIMBA": ""
}
IS_DEPLOY = False


class SummaryQueryBase():
    """General summary query base class
    """
    def __init__(self):
        pass

    def _init_teradata_connection(self, td_platform='JACKAL'): # JACKAL or SIMBA
        host = TD_CONFIG[td_platform]
        user_name = TD_CONFIG['username']
        password = TD_CONFIG['password']
        if IS_DEPLOY:
            self.td_con = TeradataOdbc(host=host, user_name=user_name, password=password)
        else:
            self.td_con = Teradata(host=host, user_name=user_name, password=password)

    def query_sample(self):
        self._init_teradata_connection()
        return self.td_con.query(query_string='''select * from pp_oap_sing_jyang2_t.test;''')

    def query(self):
        pass


td_query_instance = SummaryQueryBase()