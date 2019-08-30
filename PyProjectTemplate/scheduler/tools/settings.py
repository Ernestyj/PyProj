# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime
import pandas as pd
from pytz import timezone as tz


pd.options.mode.chained_assignment = None  # default='warn'


# project run stage (current git branch)
# PROJECT_RUNTIME_STAGE = os.environ['PROJECT_RUNTIME_STAGE']
PROJECT_RUNTIME_STAGE = 'feature'
# project fun mode (deploy/test)
# PROJECT_RUNTIME_MODE = os.environ['PROJECT_RUNTIME_MODE']
PROJECT_RUNTIME_MODE = 'test'

IS_DEPLOY = False if os.environ['IS_DEPLOY'] in ['False', 'false'] else True # TODO control is teradata odbc

# project path define
MODULE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # reaper
ROOT_PATH = os.path.dirname(MODULE_PATH)

# log path define
LOG_DIR = os.path.join(MODULE_PATH, 'log')
# log formatter defin
LOG_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# timezone settings
TIMEZONE_PST8PDT = tz('PST8PDT')
# TIMEZONE_PST8PDT = tz('US/Pacific')
TIMEZONE_CHINA = tz('Asia/Shanghai')
TIMEZONE_GMT = tz('GMT')
# time format
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# api version define
API_VERSION = "/v1"

# production stage config
PROD_CONFIG = {
    'timezone': TIMEZONE_PST8PDT,
    'logging_level': logging.WARN
}
# development stage config
DEVELOP_CONFIG = {
    'timezone': TIMEZONE_PST8PDT,
    'logging_level': logging.DEBUG,
    'mongo_alert_queue': {
        'host': 'alerts_queue_mongo',
        'port': 27017,
    },
}
# feature stage config
FEATURE_CONFIG = {
    'timezone': TIMEZONE_PST8PDT,
    'logging_level': logging.DEBUG,
    'mongo_alert_queue': {
        'host': 'alerts_queue_mongo',
        'port': 27017,
    },
}
# test mode config
TEST_CONFIG = {
    'timezone': TIMEZONE_PST8PDT,
    'logging_level': logging.DEBUG,

    'mail': {
        'host': u"",
        "port": 25,
        'senders': [u''],

        "receivers_test": [
            u'',
        ],
    },

    "teradata": {
        "username": u"",
        "password": u"",
        "JACKAL": u"",

        "username_simba": u"",
        "password_simba": u"",
        "SIMBA": u"",
    },

    "mysql_job_time": {
        "username": "rule360",
        "password": "rule360",
        "host": "",
        "defaultdb": "rule360"
    },

    'mongo_alert_queue': {
        'host': 'alerts_queue_mongo',
        'port': 27017,
    },
}
# all config
FULL_CONFIG = {
    'prod': {
        'deploy': PROD_CONFIG,
        'test': TEST_CONFIG,
    },
    'develop': {
        'deploy': DEVELOP_CONFIG,
        'test': TEST_CONFIG,
    },
    'feature': {
        'deploy': FEATURE_CONFIG,
        'test': TEST_CONFIG,
    }
}
# current config
PROJECT_CONFIG = FULL_CONFIG[PROJECT_RUNTIME_STAGE][PROJECT_RUNTIME_MODE]
TIMEZONE = FULL_CONFIG[PROJECT_RUNTIME_STAGE][PROJECT_RUNTIME_MODE]['timezone']

def define_logger(log_name, logging_level):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging_level)
    try:
        os.makedirs(os.path.sep.join([LOG_DIR, log_name]))  # make all dirs, including intermediate dirs
    # except FileExistsError:
    except Exception:
        pass
    # file handler
    fh = logging.FileHandler(os.path.sep.join([ LOG_DIR, log_name, datetime.strftime(datetime.now(TIMEZONE), '%Y%m%d.txt') ]))
    fh.setLevel(logging_level)
    fh.setFormatter(LOG_FORMATTER)
    logger.addHandler(fh)
    # terminal stream handler
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    ch.setFormatter(LOG_FORMATTER)
    logger.addHandler(ch)
    return logger


logger_ = define_logger('main', PROJECT_CONFIG['logging_level'])
