#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from minepy import MINE
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="white", context="talk")

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
upOrDowns = []
for v in R.values:
    if v>0: upOrDowns.append(1)
    else: upOrDowns.append(-1)
# print upOrDowns
print 'Day count:', len(df)
# print df.head(5)
# df['R'] = R

dfi = readWSDIndexFile(baseDir, stockCodes[i], startYear, number)
dfi['R'] = R
print np.shape(df), np.shape(dfi)

allDF = pd.concat([df, dfi], axis=1)

scaler = preprocessing.MinMaxScaler()
X_Standard = scaler.fit_transform(df)
X_Standard_T = np.transpose(X_Standard)
Xi_Standard = scaler.fit_transform(dfi)
Xi_Standard_T = np.transpose(Xi_Standard)
X_ALL_Standard = scaler.fit_transform(allDF)
X_ALL_Standard_T = np.transpose(X_ALL_Standard)
print np.shape(X_ALL_Standard_T)

mine = MINE(alpha=0.6, c=15, est="mic_approx")
mics = []
# mine.compute_score(df['Close'].values, df['R'].values); print mine.mic()
# # for i in range(0,10):
# #     mine.compute_score(X_Standard_T[i], X_Standard_T[10])
# #     mics.append(mine.mic())
# #     print i, mine.mic()
# for i in [7,9]:
#     mine.compute_score(X_Standard_T[i], X_Standard_T[10])
#     mics.append(mine.mic())
#     print i, mine.mic()
# # for i in range(0,38):
# #     mine.compute_score(Xi_Standard_T[i], Xi_Standard_T[38])
# #     mics.append(mine.mic())
# #     print i, mine.mic()
# for i in range(0,7):
#     mine.compute_score(Xi_Standard_T[i], Xi_Standard_T[7])
#     mics.append(mine.mic())
#     print i, mine.mic()
#

for i in range(48):
    mine.compute_score(X_ALL_Standard_T[i], X_ALL_Standard_T[48])
    mics.append(mine.mic())

names = []
for c in allDF.columns.values: names.append(c)

map = {}
for i in range(48):
    map[names[i]] = mics[i]

import operator
sorted_tuple = sorted(map.items(), key=operator.itemgetter(1))

vs = []
ks = []
for k,v in sorted_tuple:
    ks.append(k); vs.append(v)
ks = ks[::-1]
vs = vs[::-1]

def plotMICHist():
    f, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(ks, vs, palette="BuGn_d", ax=ax)
    ax.set_ylabel("MIC")
    plt.xticks(rotation=90)
    f.subplots_adjust(bottom=0.2)
    plt.show()