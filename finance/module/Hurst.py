#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import nolds

def readAndReWriteCSV(baseDir, instrument, startDay, endDay):
    dateparse = lambda x: pd.to_datetime(x, format='%Y-%m-%d')
    startYear = int(startDay[:startDay.find('-')])
    endYear = int(endDay[:endDay.find('-')])
    startDay = pd.to_datetime(startDay, format='%Y-%m-%d')
    endDay = pd.to_datetime(endDay, format='%Y-%m-%d')
    df = None
    for year in range(startYear, endYear + 1):
        tempDF = pd.read_csv(baseDir + instrument + '\\wsd_' + instrument + '_' + str(year) + '.csv',
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

# 路径
baseDir = 'E:\\Downloads\\Data\\'
# baseDir = '/Users/eugene/Downloads/data/'
# 股票代码
instrument = '000001.SH'
# 开始时间
startDay = '2010-01-01'
# 结束时间
endDay = '2015-06-06'

# pathName, df = readAndReWriteCSV(baseDir, instrument, startDay, endDay)
# print hurst(df['Close'])

import sys
baseDir = str(sys.argv[1])
instrument = str(sys.argv[2])
startDay = str(sys.argv[3])
endDay = str(sys.argv[4])
pathName, df = readAndReWriteCSV(baseDir, instrument, startDay, endDay)
print hurst(df['Close'])