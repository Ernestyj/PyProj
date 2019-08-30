# -*- coding: utf-8 -*-
import unittest

from td_query.td_query_base import td_query_instance as instance
from tools.settings import *


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

        df = instance.query_td_sample()
        print(df)