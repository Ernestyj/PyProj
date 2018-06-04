# -*- coding: utf-8 -*-
import logging
import traceback

from tools import JsonConf, Teradata, TeradataOdbc


class TeradataQueryBase():
    """General summary query base class
    """
    def __init__(self, conf_path, teradata_platform='JACKAL'):
        """
        :param teradata_platform: 'JACKAL' or 'SIMBA'
        """
        # init param
        self.conf_path = conf_path
        self.teradata_platform = teradata_platform
        # toggle
        self.is_prod = False
        self.use_odbc_teradata = False
        # init param placeholder
        self.logger = None
        self.conf = None
        self.conf_teradata = None
        self.teradata = None

    def init(self):
        self._init_logger()
        self._get_conf()
        self._init_connect_teradata()

    def reinit_connect_teradata(self, teradata_platform):
        self.teradata_platform = teradata_platform
        if self.use_odbc_teradata:
            self.teradata = TeradataOdbc(host=self.conf_teradata[self.teradata_platform], user_name=self.conf_teradata['username'], password=self.conf_teradata['password'])
        else:
            self.teradata = Teradata(host=self.conf_teradata[self.teradata_platform], user_name=self.conf_teradata['username'], password=self.conf_teradata['password'])

    def query_sample(self):
        return self.teradata.query(query_string='''select * from pp_oap_sing_jyang2_t.test;''')

    def query(self, query_string):
        self.logger.info('Start  querying, query="{}"'.format(query_string))
        df = self.teradata.query(query_string=query_string)
        self.logger.info('Finish querying, query="{}"'.format(query_string))
        return df

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
            self.conf_teradata = self.conf['teradata']
            self.is_prod = True if self.conf['mail_alert']['is_prod'] == 'true' else False
            if self.is_prod:
                self.use_odbc_teradata = True
        except Exception as e:
            traceback.print_exc()
            self.logger.error(e.message)

    def _init_connect_teradata(self):
        if self.use_odbc_teradata:
            self.teradata = TeradataOdbc(host=self.conf_teradata[self.teradata_platform], user_name=self.conf_teradata['username'], password=self.conf_teradata['password'])
        else:
            self.teradata = Teradata(host=self.conf_teradata[self.teradata_platform], user_name=self.conf_teradata['username'], password=self.conf_teradata['password'])

    # query helper##############################################################################
    def _generate_subquery(self):
        pass

    def generate_query(self):
        pass