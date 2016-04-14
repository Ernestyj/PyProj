#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf


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
        tempDF = pd.read_csv(baseDir+stockCode+'/wsd_'+stockCode+'_'+str(startYear+i)+'.csv',
                                index_col=0, sep='\t', usecols=[0,2,3,4,5,6], header=None,
                                skiprows=1, names=['DATE','OPEN','HIGH','LOW','CLOSE','VOLUME'],
                               parse_dates=True, date_parser=dateparse)
        if i==0: df = tempDF
        else: df = df.append(tempDF)
    return df

'''
读入一组股票指定年份的ohlcv数据
输入:baseDir为字符,stockCodes为股票代码数组, startYear,yearNum为整数，
输出:dataframe
'''
def concatWSDFile(baseDir, stockCodes, startYear, yearNum=1):
    def readAllWSDFile(stockCode):
        return readWSDFile(baseDir, stockCode, startYear, yearNum)
    dfs = map(readAllWSDFile, stockCodes)
    return pd.concat(dfs, keys=stockCodes, names=['Code', 'Date'])

# baseDir = '/Users/eugene/Downloads/marketQuotationData/'
# stockCodes = ['000001.SZ', '000002.SZ', '000004.SZ', '000005.SZ', '000006.SZ']

# baseDir = '/Users/eugene/Downloads/data/'
# stockCodes = ['000001.SH', '000300.SH', '000905.SH']
#
# wsd_000001SZ_2012_2015 = readWSDFile(baseDir, stockCodes[0], 2012, 4)
# print wsd_000001SZ_2012_2015.sample(5)
#
# wsd_2012_2015 = concatWSDFile(baseDir, stockCodes, 2012, 4)
# print wsd_2012_2015.sample(5)