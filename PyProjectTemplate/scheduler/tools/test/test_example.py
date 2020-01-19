# -*- coding: utf-8 -*-
import unittest


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

    def test_example(self):
        x = []
        # print(x[1])
        print("This is a test example.")
