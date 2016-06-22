#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
# sns.set(context="paper", font="monospace")

from sklearn import preprocessing

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 30)
pd.set_option('precision', 7)
pd.options.display.float_format = '{:,.3f}'.format
import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)


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
                                index_col=0, sep='\t', usecols=[0,2,3,4,5,6,7,9,10,12,15], header=None,
                                skiprows=1, names=['Date','Open','High','Low','Close','Volume','Amount',
                                                   'Chg','Chg Pct','Avg','Turn'],
                               parse_dates=True, date_parser=dateparse)
        if i==0: df = tempDF
        else: df = df.append(tempDF)
    return df


usecols = [0, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
           21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 36, 37]
# usecols = [0, 6, 16, 17, 24, 31]
usecols = [0, 2,11,24,26,29,30]
# usecols = [0, 5,7,11,19,24,26,28]
def readWSDIndexFile(baseDir, stockCode, startYear, yearNum=1):
    # 解析日期
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d').date()

    df = 0
    for i in range(yearNum):
        tempDF = pd.read_csv(baseDir+'I'+stockCode+'/wsd_'+stockCode+'_'+str(startYear+i)+'.csv',
                                index_col=0, sep=',', parse_dates=True, date_parser=dateparse
                             # , usecols=usecols
                             )
        if i==0: df = tempDF
        else: df = df.append(tempDF)
    return df


baseDir = '/Users/eugene/Downloads/data/'
stockCodes = ['000300.SH', '000016.SH', '000905.SH']

i = 0
startYear = 2014
number = 2
df = readWSDFile(baseDir, stockCodes[i], startYear, number)
R = df['Close'].pct_change()
R[0] = R[1]
# upOrDowns = []
# for v in R.values:
#     if v>0: upOrDowns.append(1)
#     else: upOrDowns.append(-1)
# # print upOrDowns
print 'Day count:', len(df)
# df['R'] = R

dfi = readWSDIndexFile(baseDir, stockCodes[i], startYear, number)
# dfi['R'] = df['R']
print np.shape(df), np.shape(dfi)

allDF = pd.concat([df, dfi], axis=1)
# print allDF.head(3)

def plotCorrHeatmap(allDF):
    corrmat = allDF.corr()
    f, ax = plt.subplots(figsize=(12, 9))
    mask =  np.tri(corrmat.shape[0], k=-1)
    cmap = plt.cm.get_cmap('RdBu') # jet doesn't have white color
    cmap.set_bad('w') # default value is 'k'
    sns.heatmap(corrmat, square=False, mask=mask.T, cmap=cmap)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.show()


plotCorrHeatmap(allDF)