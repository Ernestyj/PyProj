#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import zipline as zp
import talib
import math
from datetime import datetime

'''
读入一支股票指定年份的ohlcv数据
输入:baseDir,stockCode为字符, startYear,yearNum为整数，
输出:dataframe
'''


def readWSDFile(baseDir, stockCode, startYear, yearNum=1):
    # 解析日期
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d').date()

    df = 0
    for i in range(yearNum):
        tempDF = pd.read_csv(baseDir + stockCode + '/wsd_' + stockCode + '_' + str(startYear + i) + '.csv',
                             index_col=0, sep='\t', usecols=[0, 2, 3, 4, 5, 6], header=None,
                             skiprows=1, names=['Date', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'],
                             parse_dates=True, date_parser=dateparse)
        if i == 0:
            df = tempDF
        else:
            df = df.append(tempDF)
    return df


baseDir = '/Users/eugene/Downloads/data/'
stockCodes = ['000001.SH']
wsd = readWSDFile(baseDir, stockCodes[0], 2010, 5)
wsdClose = wsd['CLOSE']
wsdClose.index = wsdClose.index.tz_localize('UTC')
wsdVolume = wsd['VOLUME']
wsdVolume.index = wsdVolume.index.tz_localize('UTC')
wsdOpen = wsd['OPEN']
wsdOpen.index = wsdOpen.index.tz_localize('UTC')
wsdHigh = wsd['HIGH']
wsdHigh.index = wsdHigh.index.tz_localize('UTC')
wsdLow = wsd['LOW']
wsdLow.index = wsdLow.index.tz_localize('UTC')

import zipline
from zipline import TradingAlgorithm
from zipline.api import *

code = '000001.SH'
shortWin = 30
longWin = 100
data = pd.Panel({'000001.SH': pd.DataFrame(
    {'open': wsdOpen, 'high': wsdHigh, 'low': wsdLow, 'close': wsdClose, 'volume': wsdVolume, 'price': wsdClose})})


def initialize(context):
    add_history(shortWin, '1d', 'price')
    add_history(longWin, '1d', 'price')
    context.day = 0
    set_slippage(slippage.VolumeShareSlippage(volume_limit=1.0, price_impact=0.0))
    set_commission(commission.PerDollar(cost=0.003))


def handle_data(context, data):
    # print context.portfolio.cash
    context.day += 1

    if context.day < longWin:
        return

    print context.day
    shortClose = history(shortWin, '1d', 'price')
    print shortClose
    shortClose = shortClose.iloc[:, 0].values
    shortMA = talib.SMA(shortClose, shortWin)
    # print(shortMA)
    longClose = history(longWin, '1d', 'price')
    # print longClose
    longClose = longClose.iloc[:, 0].values
    longMA = talib.SMA(longClose, longWin)
    # print(longMA)
    if shortMA[-1] > longMA[-1]:
        order_percent(symbol(code), 1.0)
    elif shortMA[-1] < longMA[-1]:
        order_percent(symbol(code), -1.0)


algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
perf = algo.run(data)
