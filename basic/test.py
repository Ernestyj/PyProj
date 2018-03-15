#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json


print "******start******"
x=['ttl_MYSQL', 'ttl_TD']
print x.extend(['ttl_MYSQL', 'ttl_TD'])
print x


PYTHON_MODULE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_PATH = os.path.dirname(PYTHON_MODULE_PATH)
print PYTHON_MODULE_PATH
print ROOT_PATH

json_str = """{}
"""
print json.dumps(json_str)