# -*- coding: utf-8 -*-
import unittest

from tools.settings import *


# from mysql_query.td_job_time_used_query import job_time_used_query_instance as instance


class TestExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("**************************************** setUpClass ****************************************")

    @classmethod
    def tearDownClass(cls):
        print("************************************** tearDownClass ***************************************")

    def setUp(self):
        print("****** setUp *******")

    def tearDown(self):
        print("***** tearDown *****")

    def _example(self):
        print("This is a test example.")
        print(TIMEZONE)

        # df_time_used = instance.query()
        # print(df_time_used)