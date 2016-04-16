#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

'''
将x轴转化为均匀分布的时间刻度(跳过没有数据的日期)
'''
from matplotlib.ticker import Formatter
class MyFormatter(Formatter):
    def __init__(self, dates, fmt='%Y-%m-%d'):
        self.dates = dates
        self.fmt = fmt

    def __call__(self, x, pos=0):
        'Return the label for time x at position pos'
        indices = int(round(x))
        if indices>=len(self.dates) or indices<0: return ''
        return self.dates[indices].strftime(self.fmt)

'''
绘制时间序列图形,x轴为时间刻度(跳过没有数据的日期)
输入:df,注意df的index为时间
输出:
'''
def plotWithXDate(df, figureSize=(20,5), tickWin=5):
    fig,ax = plt.subplots(figsize=figureSize)
    ax.plot(np.arange(len(df)), df)
    ax.xaxis.set_ticks(np.arange(0, len(df), tickWin))
    ax.xaxis.set_major_formatter(MyFormatter(df.index))
    #start,end = ax.get_xlim()
    #print start,end,len(df)
    ax.set_xlim(0, len(df)-1)
    fig.autofmt_xdate()
    plt.show()


'''
根据ohlcDF产生ohlcTuple,包含时间的转化(为candlestick_ohlc绘图准备参数)
输入:ohlcDF
输出:ohlcTuple
'''
def ohlcTuple(ohlcDF):
    ohlcDF = ohlcDF.reset_index()
    import matplotlib.dates as mdates
    # 将日期转换成时间浮点数
    dateToFloat = lambda date: mdates.date2num(date.to_pydatetime())
    ohlcDF['date_float'] = ohlcDF['Date'].apply(dateToFloat)
    return [tuple(t) for t in ohlcDF[['date_float', 'OPEN', 'HIGH', 'LOW', 'CLOSE']].values]

'''
绘制K线图(带有weekends间隔)
输入:ohlcDF
输出:
'''
def plotK(ohlcDF):
    ohlctuple = ohlcTuple(ohlcDF)

#     from matplotlib.dates import (WeekdayLocator, MONDAY)
#     mondays = WeekdayLocator(MONDAY)  # x axis label major ticks on Monday
#     from matplotlib.dates import DateFormatter
#     week_fomatter = DateFormatter('%b %d') #Jan 12

    from matplotlib.finance import candlestick_ohlc
    fig, ax = plt.subplots(figsize=(20,6))
    candlestick_ohlc(ax, ohlctuple, width=0.6, colorup='g', colordown='r')
    ax.xaxis_date() # 默认x轴显示为日期
#     ax.xaxis.set_major_locator(mondays)
#     ax.xaxis.set_major_formatter(week_fomatter)
    plt.grid(True)
    fig.autofmt_xdate() # 自动调整x轴日期显示效果
    ax.autoscale_view()

'''
绘制K线图(不带weekends间隔)
输入:ohlcDF
输出:
'''
def plotKWithNoGap(ohlcDF, figureSize=(30,8), tickWin=5):
    from matplotlib.finance import candlestick2_ohlc
    fig, ax = plt.subplots(figsize=figureSize)
    candlestick2_ohlc(ax, ohlcDF['OPEN'], ohlcDF['HIGH'], ohlcDF['LOW'], ohlcDF['CLOSE'], width=0.7, colorup='g', colordown='r')
    ax.xaxis.set_ticks(np.arange(0, len(ohlcDF), tickWin))
    ax.xaxis.set_major_formatter(MyFormatter(ohlcDF.index))
    ax.set_xlim(-1, len(ohlcDF))
    fig.autofmt_xdate() # 自动调整x轴日期显示效果
    plt.grid(True)
    plt.show()


'''
绘制MACD图(不带weekends间隔)
输入:macdDF
输出:
'''
def plotMACD(macdDF, figureSize=(20,6), tickWin=5):
    fig, ax = plt.subplots(figsize=figureSize)
    x = np.arange(len(macdDF))
    columnNames = macdDF.columns.values
    ax.plot(x, macdDF[columnNames[0]], 'g') #DIF
    ax.plot(x, macdDF[columnNames[1]], 'r') #DEM
    ax.bar(x, macdDF[columnNames[3]]) #OSC
    ax.xaxis.set_ticks(np.arange(0, len(macdDF), tickWin))
    ax.xaxis.set_major_formatter(MyFormatter(macdDF.index))
    ax.set_xlim(0, len(macdDF))
    fig.autofmt_xdate()
    plt.legend()
    plt.show()



