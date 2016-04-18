#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

'''
计算收益率
输入:V, C
输出:收益率
'''
def returnRatio(V, C=100000.0):
    return V/C-1.0

'''
计算收益率
输入:V数组, C
输出:收益率数组
'''
def returnRatioArr(VArr, C=100000.0):
    arr = []
    for v in VArr: arr.append(v/C-1.0)
    return arr

'''
计算有效投资天数
输入:买入df, 卖出df, 模拟投资结果perf(df的索引为时间)
输出:收益率
'''
def validInvestDays(buys, sells, perf):
    days = 0
    for i in range(len(sells)):
        days += (sells.index[i]-buys.index[i]).days
    if len(buys)>len(sells):
        days += (perf.index[-1]-buys.index[-1]).days
    return days

'''
计算年化收益率
输入:收益率数组, T, D
输出:年化收益率
'''
def annualizedReturnRatio(returnRatioArr, T=250.0, D=250.0):
    import math
    tmp = 1
    for r in returnRatioArr: tmp *= (r+1)
    return math.pow(tmp, D/T)-1

'''
计算MA
输入:
输出:DataFrame
'''
def MA(closeSeries, shortWin=5, longWin=20):
    shortMA = pd.rolling_mean(closeSeries, window=shortWin)
    longMA = pd.rolling_mean(closeSeries, window=longWin)
    return pd.DataFrame({'Close': closeSeries, str(shortWin)+'MA':shortMA, str(longWin)+'MA': longMA})


'''
计算EMA/EWMA
输入:
输出:DataFrame
'''
def EWMA(closeSeries, shortWin=12, longWin=26):
    shortEWMA = pd.ewma(closeSeries, span=shortWin)
    longEWMA = pd.ewma(closeSeries, span=longWin)
    return pd.DataFrame({'Close': closeSeries, str(shortWin)+'EWMA':shortEWMA, str(longWin)+'EWMA': longEWMA})


'''
计算MACD
输入:
输出:DataFrame
'''
def MACD(closeSeries, shortWin=12, longWin=26, DIFWin=9):
    shortEWMA = pd.ewma(closeSeries, span=shortWin)
    longEWMA = pd.ewma(closeSeries, span=longWin)
    DIF = shortEWMA-longEWMA
    DEM = pd.ewma(DIF, span=DIFWin)
    OSC = DIF-DEM
    return pd.DataFrame({'Close':closeSeries, str(shortWin)+'/'+str(longWin)+'DIF':DIF,
                         str(DIFWin)+'DEM':DEM, 'OSC':OSC})