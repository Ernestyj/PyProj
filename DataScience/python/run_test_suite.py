# -*- coding: utf-8 -*-
import unittest

from tools.test.test_json_tools import TestJsonTools
from tools.test.test_td_tools import TestTdTools
from td_query.test.test_example import TestExample
from td_query.test.test_data_manipulate import TestDataManipulate

if __name__ == '__main__':
    suite = unittest.TestSuite()

    ## loadTestsFromNames()，传入列表
    # suite.addTests(unittest.TestLoader().loadTestsFromNames(['tools.test.test_json_tools.TestJsonTools']))
    ### loadTestsFromName()，传入'模块名.TestCase名'
    # suite.addTests(unittest.TestLoader().loadTestsFromName('tools.test.test_json_tools.TestJsonTools'))

    ### loadTestsFromTestCase()，传入TestCase
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestJsonTools))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTdTools))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestExample))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDataManipulate))

    ### 用addTests方法添加多个TestCase
    # suite.addTests(tests=[TestJsonTools("test_get_json_conf")])

    ### 直接用addTest方法添加单个TestCase
    # suite.addTest(TestJsonTools("test_get_json_conf"))
    # suite.addTest(TestCfTdJobAlert("test_conf"))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
