#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

import ReadData

sys.path.append('/Users/eugene/ProgramData/PyStudy/finance')

baseDir = '/Users/eugene/Downloads/data/'
stockCodes = ['000001.SH', '000300.SH', '000905.SH']

wsd_000001SZ_2012_2015 = ReadData.readWSDFile(baseDir, stockCodes[0], 2012, 4)
print wsd_000001SZ_2012_2015.sample(5)

wsd_2012_2015 = ReadData.concatWSDFile(baseDir, stockCodes, 2012, 4)
print wsd_2012_2015.sample(5)
