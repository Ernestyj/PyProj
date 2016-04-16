#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

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