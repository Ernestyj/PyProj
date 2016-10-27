#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os
import datetime

def readAndReWriteCSV(baseDir, instrument, startDay, endDay):
    dateparse = lambda x: pd.to_datetime(x, format='%Y-%m-%d')
    startYear = int(startDay[:startDay.find('-')])
    endYear = int(endDay[:endDay.find('-')])
    startDay = pd.to_datetime(startDay, format='%Y-%m-%d')
    endDay = pd.to_datetime(endDay, format='%Y-%m-%d')
    df = None
    for year in range(startYear, endYear + 1):
        tempDF = pd.read_csv(baseDir + instrument + os.path.sep + 'wsd_' + instrument + '_' + str(year) + '.csv',
                             index_col=0, sep='\t', usecols=[0, 2, 3, 4, 5, 6, 14], header=None,
                             skiprows=1, names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'],
                             parse_dates=True, date_parser=dateparse)
        if df is None:
            df = tempDF
        else:
            df = df.append(tempDF)
    pathName = 'temp.csv'
    resultDF = df[startDay:endDay]
    resultDF.to_csv(pathName)
    return pathName, resultDF

from numpy import cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn
def hurst(ts):
	"""Returns the Hurst Exponent of the time series vector ts"""
	# Create the range of lag values
	lags = range(2, 100)
	# Calculate the array of the variances of the lagged differences
	tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
	# Use a linear fit to estimate the Hurst Exponent
	poly = polyfit(log(lags), log(tau), 1)
	# Return the Hurst exponent from the polyfit output
	return poly[0]*2.0

# 移动平均hurst指数计算
# 例如计算120个交易日的Husrt指数，使用的数据为[t-119,t]的价格数据即可，移动平均的意思为根据t的向前移动，
# 计算指数的数据[t-119,t]的价格数据同时根据t进行移动。
'''
输入：以时间为索引的Series
输出：以时间为索引的hurst Series
'''
def computeMovingHurst(dataSeries, window=233):
    dataLen = len(dataSeries)
    if dataLen<window:
        print 'window length is bigger than data length'
        return
    hursts = np.zeros(dataLen)
    hursts[0:window] = np.NaN
    for i in range(dataLen-window):
        hursts[window+i] = hurst(dataSeries[i:i+window])
    return pd.Series(hursts, index=dataSeries.index)


# 路径
baseDir = 'E:\\Downloads\\Data\\'
# baseDir = '/Users/eugene/Downloads/data/'
# 股票代码
instrument = '000001.SH'
# 开始时间
startDay = '2013-01-01'
# 结束时间
endDay = '2015-06-06'
# Hurst计算窗口
window = 233

import sys
baseDir = str(sys.argv[1])
instrument = str(sys.argv[2])
startDay = str(sys.argv[3])
endDay = str(sys.argv[4])
window = int(sys.argv[5])

startDayWithWindow = pd.to_datetime(startDay, format='%Y-%m-%d')
startDayWithWindow = startDayWithWindow + datetime.timedelta(days=-window*2) #指定日期+窗口*2的数据
pathName, df = readAndReWriteCSV(baseDir, instrument, startDayWithWindow.strftime('%Y-%m-%d'), endDay)
startDay = pd.to_datetime(startDay, format='%Y-%m-%d')
print [date.strftime('%Y-%m-%d') for date in df[startDay:].index]  #日期
print df[startDay:]['Close'].values.tolist()    #收盘价
hursts = computeMovingHurst(df['Close'], window).values.tolist()  #移动Hurst指数
print hursts[-len(df[startDay:]):]
