# -*- coding: utf-8 -*-
import unittest

from tools.test.summary_query_base import td_query_instance as instance


class TestSummaryQueryBase(unittest.TestCase):
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

        result = instance.query_sample()
        print(result)