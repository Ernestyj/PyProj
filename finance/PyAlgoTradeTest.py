#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib

from pyalgotrade import strategy, plotter
from pyalgotrade.broker.backtesting import TradePercentage, Broker
from pyalgotrade.broker import Order
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.broker.slippage import NoSlippage, VolumeShareSlippage
from pyalgotrade.stratanalyzer import returns, trades
from pyalgotrade.talibext import indicator

def readAndReWriteCSV(baseDir, instrument, startYear, yearNum=1):
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d').date()
    df = 0
    for i in range(yearNum):
        tempDF = pd.read_csv(baseDir + instrument + '/wsd_' + instrument + '_' + str(startYear + i) + '.csv',
                             index_col=0, sep='\t', usecols=[0, 2, 3, 4, 5, 6, 14], header=None,
                             skiprows=1, names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'],
                             parse_dates=True, date_parser=dateparse)
        if i == 0:
            df = tempDF
        else:
            df = df.append(tempDF)
    pathName = None
    resultDF = None
    if yearNum==1:
        pathName = baseDir+str(instrument)+'_'+str(startYear)+'.csv'
        resultDF = df[str(startYear)]
    else:
        pathName = baseDir+str(instrument)+'_'+str(startYear)+'_'+str(startYear+yearNum-1)+'.csv'
        resultDF = df[str(startYear):str(startYear+yearNum-1)]
    resultDF.to_csv(pathName)
    return pathName, resultDF

'''
计算收益率
'''
def returnRatio(V, C=100000.0):
    return V/C-1.0

'''
计算收益率
'''
def returnRatioArr(VArr, C=100000.0):
    arr = []
    for v in VArr: arr.append(v/C-1.0)
    return arr

'''
计算年化收益率
'''
def annualizedReturnRatio(returnRatioArr, T=250.0, D=250.0):
    import math
    tmp = 1
    for r in returnRatioArr: tmp *= (r+1)
    return math.pow(tmp, D/T)-1


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, df, shortWin=20, longWin=40):
        super(MyStrategy, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        self.getBroker().setCash(100000)
        self.getBroker().setCommission(TradePercentage(0.003))
        self.getBroker().setAllowNegativeCash(True)
        self.getBroker().getFillStrategy().setVolumeLimit(1)
        self.getBroker().getFillStrategy().setSlippageModel(VolumeShareSlippage(priceImpact=0.0))
        self.__closeDataSeries = feed[instrument].getCloseDataSeries()
        self.df = df
        self.shortWin = shortWin
        self.longWin = longWin
        self.closeArr = []
        self.fastSMA = []
        self.slowSMA = []
        self.buys = []
        self.sells = []
        self.portfolios = []

    def getDF(self):
        return self.df

    def getBuys(self):
        return self.buys

    def getSells(self):
        return self.sells

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("%s BUY %.0f shares at %.3f, commission=%.3f, PnL=%.3f" %
                  (execInfo.getDateTime().date(), execInfo.getQuantity(), execInfo.getPrice(), execInfo.getCommission(), position.getPnL()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("%s SELL %.0f shares at %.3f, commission=%.3f, PnL=%.3f" %
                  (execInfo.getDateTime().date(), execInfo.getQuantity(), execInfo.getPrice(), execInfo.getCommission(), position.getPnL()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onStart(self):
        pass

    def onFinish(self, bars):
        self.df['closeArr'] = self.closeArr
        self.df['fastSMA'] = self.fastSMA
        self.df['slowSMA'] = self.slowSMA
        self.df['portfolio'] = self.portfolios
        # print self.df[['Close', 'closeArr', 'fastSMA', 'slowSMA', 'portfolio']].sample(5)
        pass

    def onOrderUpdated(self, order):
        execInfo = order.getExecutionInfo()
        fillDate = None
        if execInfo!=None:
            fillDate = execInfo.getDateTime().date()
            if order.getAction()==1: self.buys.append(fillDate)
            else: self.sells.append(fillDate)
        print 'id=',order.getId(), 'state=',Order.State.toString(order.getState()), 'type=',order.getType(), \
            'submitAt=',order.getSubmitDateTime().date(), 'fillAt=',fillDate, \
            'action=',order.getAction(), 'state=',order.getState(), 'active=',order.isActive(), \
            'quantity=',order.getQuantity(), 'Positions=',self.getBroker().getPositions(), \
            'cash=', self.getBroker().getCash()

    def onBars(self, bars):
        self.closeArr.append(bars[self.__instrument].getPrice())
        self.portfolios.append(self.getBroker().getEquity())

        if len(self.closeArr)<self.longWin:
            self.fastSMA.append(np.nan)
            self.slowSMA.append(np.nan)
            return

        # fast_sma = indicator.SMA(self.__closeDataSeries, self.shortWin, self.shortWin)
        # slow_sma = indicator.SMA(self.__closeDataSeries, self.longWin, self.longWin)
        fast_sma = talib.SMA(np.array(self.closeArr[-self.shortWin:]), self.shortWin)
        slow_sma = talib.SMA(np.array(self.closeArr[-self.longWin:]), self.longWin)

        self.fastSMA.append(fast_sma[-1])
        self.slowSMA.append(slow_sma[-1])

        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if fast_sma[-1] > slow_sma[-1]:
                shares = int(self.getBroker().getCash() / bars[self.__instrument].getPrice())
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, False)
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and fast_sma[-1] < slow_sma[-1]:
            self.__position.exitMarket()


baseDir = '/Users/eugene/Downloads/Data/'
# baseDir = '/Users/eugene/Downloads/marketQuotationData/'
instruments = ['000001.SH', '000300.SH', '000001.SZ']
instrument = instruments[0]
pathName, df = readAndReWriteCSV(baseDir, instrument, 2015, yearNum=1)
print pathName
# print df.sample(3)

feed = yahoofeed.Feed()
feed.addBarsFromCSV(instrument, pathName)

myStrategy = MyStrategy(feed, instrument, df=df, shortWin=20, longWin=40)

returnsAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(returnsAnalyzer)
tradesAnalyzer = trades.Trades()
myStrategy.attachAnalyzer(tradesAnalyzer)

myStrategy.run()

df = myStrategy.getDF()
# print df[['Close', 'closeArr', 'fastSMA', 'slowSMA']].sample(5)
buys = myStrategy.getBuys()
sells = myStrategy.getSells()
print 'TRADE INFO: ', 'count=',tradesAnalyzer.getCount(), 'allProfits=',tradesAnalyzer.getAll(), 'allReturns=',tradesAnalyzer.getAllReturns()
myStrategy.critical("总净值: %.3f" % myStrategy.getResult())
myStrategy.critical("总收益率: %.3f" % returnRatio(myStrategy.getResult(), C=100000.0))
myStrategy.critical("年化收益率: %.3f" % annualizedReturnRatio(returnRatioArr(df['portfolio'].ix[sells].values), T=250.0, D=250.0))


# fig = plt.figure(figsize=(20,20))
# ax1 = fig.add_subplot(311)
# df[['closeArr', 'fastSMA', 'slowSMA']].plot(ax=ax1, lw=2.)
# ax1.plot(buys, df.fastSMA.ix[buys], '^', markersize=10, color='m')
# ax1.plot(sells, df.fastSMA.ix[sells], 'v', markersize=10, color='k')
# ax2 = fig.add_subplot(312)
# df['portfolio'].plot(ax=ax2, lw=2.)
# ax2.plot(buys, df['portfolio'].ix[buys], '^', markersize=10, color='m')
# ax2.plot(sells, df['portfolio'].ix[sells], 'v', markersize=10, color='k')
# ax3 = fig.add_subplot(313)
# portfolio_ratio = df['portfolio']/100000.0
# portfolio_ratio.plot(ax=ax3, lw=2.)
# ax3.plot(buys, portfolio_ratio.ix[buys], '^', markersize=10, color='m')
# ax3.plot(sells, portfolio_ratio.ix[sells], 'v', markersize=10, color='k')
# plt.show()
