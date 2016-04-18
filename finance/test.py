#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

import ReadData, TechIndex

sys.path.append('/Users/eugene/ProgramData/PyStudy/finance')

baseDir = '/Users/eugene/Downloads/data/'
stockCodes = ['000001.SH', '000300.SH', '000905.SH']

wsd_000001SZ_2012_2015 = ReadData.readWSDFile(baseDir, stockCodes[0], 2012, 4)
print wsd_000001SZ_2012_2015.sample(5)

wsd_2012_2015 = ReadData.concatWSDFile(baseDir, stockCodes, 2012, 4)
print wsd_2012_2015.sample(5)

import zipline
from zipline.api import (
    add_history,
    history,
    order_target,
    record,
    symbol,
)


def initialize(context):
    # Register 2 histories that track daily prices,
    # one with a 100 window and one with a 300 day window
    zipline.api.add_history(100, '1d', 'price')
    add_history(300, '1d', 'price')
    context.i = 0


def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300:
        return

    # Compute averages
    # history() has to be called with the same params
    # from above and returns a pandas dataframe.
    short_mavg = history(100, '1d', 'price').mean()
    long_mavg = history(300, '1d', 'price').mean()

    sym = symbol('AAPL')

    # Trading logic
    if short_mavg[sym] > long_mavg[sym]:
        # order_target orders as many shares as needed to
        # achieve the desired number of shares.
        order_target(sym, 100)
    elif short_mavg[sym] < long_mavg[sym]:
        order_target(sym, 0)

    # Save values for later inspection
    record(AAPL=data[sym].price,
           short_mavg=short_mavg[sym],
           long_mavg=long_mavg[sym])

