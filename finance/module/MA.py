#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import talib
import os
from pyalgotrade import strategy, plotter
from pyalgotrade.broker.backtesting import TradePercentage, Broker
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.broker.slippage import VolumeShareSlippage
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.broker import Order


class MAStrategy(strategy.BacktestingStrategy):

    def __init__(self, feed, instrument, cash, tradePercentage, data, fastPeriod, slowPeriod):
        super(MAStrategy, self).__init__(feed)
        self.instrument = instrument
        self.invested = False
        self.shortMA = talib.SMA(data, fastPeriod)
        self.longMA = talib.SMA(data, slowPeriod)
        self.day = -1
        self.getBroker().getFillStrategy().setVolumeLimit(1)
        self.getBroker().setCommission(TradePercentage(tradePercentage))
        self.getBroker().setCash(cash)
        self.getBroker().setAllowNegativeCash(True)
        self.buys = []
        self.sells = []
        self.portfolios = []

    def onOrderUpdated(self, order):
        execInfo = order.getExecutionInfo()
        fillDate = None
        if execInfo != None:
            fillDate = execInfo.getDateTime().date()
            if order.getAction() == Order.Action.BUY:
                self.buys.append(
                    [fillDate, execInfo.getPrice(), execInfo.getQuantity()])
            if order.getAction() == Order.Action.SELL:
                self.sells.append(
                    [fillDate, execInfo.getPrice(), execInfo.getQuantity()])

    def onBars(self, bars):
        self.day = self.day + 1
        self.portfolios.append(self.getBroker().getEquity())
        bar = bars.getBar(self.instrument)
        if(bar == None or bar.getVolume() <= 0):
            return
        if np.isnan(self.shortMA[self.day]) or np.isnan(self.longMA[self.day]):
            return
        if self.shortMA[self.day] > self.longMA[self.day] and not self.invested:
            quantity = int(self.getBroker().getCash() /
                           bars[self.instrument].getPrice() / 100) * 100
            self.position = self.enterLong(self.instrument, quantity)
            self.invested = True
        if self.shortMA[self.day] < self.longMA[self.day] and self.invested:
            self.position.exitMarket()
            self.invested = False


def dayMABacktest(feed, instrument, cash, tradePercentage, df, fastPeriod, slowPeriod):
    myStrategy = MAStrategy(feed, instrument, cash, tradePercentage, df[
                            'Close'].values, fastPeriod, slowPeriod)
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
    myStrategy.run()

    # date
    print([date.strftime('%Y-%m-%d') for date in df.index])
    # close
    print(df['Close'].values.tolist())
    # buys
    print([[buy[0].strftime('%Y-%m-%d'), buy[1], buy[2]]
           for buy in myStrategy.buys])
    # sells
    print([[sell[0].strftime('%Y-%m-%d'), sell[1], sell[2]]
           for sell in myStrategy.sells])
    # portfolios
    print(myStrategy.portfolios)
    # totalValue
    print(myStrategy.portfolios[-1])
    # totalReturn
    print(returnsAnalyzer.getCumulativeReturns()[-1])
    # annualizedReturn
    print(pow(returnsAnalyzer.getCumulativeReturns()[-1] + 1,
              250.0 / len(myStrategy.portfolios)) - 1)


def readAndReWriteCSV(baseDir, instrument, startDay, endDay):
    dateparse = lambda x: pd.to_datetime(x, format='%Y-%m-%d')
    startYear = int(startDay[:startDay.find('-')])
    endYear = int(endDay[:endDay.find('-')])
    startDay = pd.to_datetime(startDay, format='%Y-%m-%d')
    endDay = pd.to_datetime(endDay, format='%Y-%m-%d')
    df = None
    for year in range(startYear, endYear + 1):
        tempDF = pd.read_csv(baseDir + instrument + '/wsd_' + instrument + '_' + str(year) + '.csv',
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


# 路径
# baseDir = 'marketQuotationData/'
baseDir = '/Users/eugene/Downloads/data/'
# 股票代码
instrument = '000001.SZ'
# 开始时间
startDay = '2010-06-01'
# 结束时间
endDay = '2013-06-06'
# 本金
cash = 1000000.0
# 手续费
tradePercentage = 0.003
# 短周期
fastPeriod = 2
# 长周期
slowPeriod = 20

# pathName, df = readAndReWriteCSV(baseDir, instrument, startDay, endDay)
# feed = yahoofeed.Feed()
# feed.addBarsFromCSV(instrument, pathName)
# dayMABacktest(feed, instrument, cash, tradePercentage, df, fastPeriod, slowPeriod)

import sys
baseDir = str(sys.argv[1])
instrument = str(sys.argv[2])
startDay = str(sys.argv[3])
endDay = str(sys.argv[4])
cash = float(sys.argv[5])
tradePercentage = float(sys.argv[6])
fastPeriod = int(sys.argv[7])
slowPeriod = int(sys.argv[8])
pathName, df = readAndReWriteCSV(baseDir, instrument, startDay, endDay)
feed = yahoofeed.Feed()
feed.addBarsFromCSV(instrument, pathName)
dayMABacktest(feed, instrument, cash, tradePercentage, df, fastPeriod, slowPeriod)
