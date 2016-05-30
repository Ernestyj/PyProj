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
from pyalgotrade.optimizer import server, local
import itertools

from sklearn import preprocessing, svm, cross_validation, metrics, pipeline, grid_search
from scipy.stats import sem

from MonthDataPrepare import readWSDFile, prepareData, optimizeSVM, readWSDIndexFile, readAndCombineMacroEconomyFile, readMoneySupplyFile


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
计算收益率(多期)
'''
def returnRatioArr1(VArr, C=100000.0):
    arr = []
    for v in VArr: arr.append(v/C-1.0)
    return arr

def returnRatioArr(VArr, C=100000.0):
    arr = []
    for v in VArr:
        arr.append(v / C - 1.0)
        C = v
    return arr

'''
计算年化收益率(多期)
'''
def annualizedReturnRatio(returnRatioArr, T=250.0, D=250.0):
    import math
    tmp = 1
    for r in returnRatioArr: tmp *= (r+1)
    return math.pow(tmp, D/T)-1

'''
计算年化收益率(单期)
'''
def annualizedReturnRatioSingle(portfolio, C=100000.0, T=250.0, D=250.0):
    import math
    return math.pow(portfolio/C, D/T) - 1


baseDir = '/Users/eugene/Downloads/Data/'
# baseDir = '/Users/eugene/Downloads/marketQuotationData/'
# 沪深300 上证50 中证500
instruments = ['000300.SH', '000016.SH', '000905.SH']
instrument = instruments[0]
initCapital = 100000000.0 # 一亿
# startYear = 2015; yearNum = 1
startYear = 2014; yearNum = 2

df = readWSDFile(baseDir, instrument, startYear=startYear, yearNum=yearNum)
print 'Day count:', len(df)
dfi = readWSDIndexFile(baseDir, instrument, startYear, yearNum)
dfmacro = readAndCombineMacroEconomyFile(baseDir, startYear, yearNum=yearNum)
dfmoney = readMoneySupplyFile(baseDir, 'money_supply.csv', startYear, yearNum=yearNum)
X, y, actionDates = prepareData(df, dfi, dfmacro, dfmoney)
print np.shape(X), np.shape(y)

normalizer = preprocessing.Normalizer().fit(X)  # fit does nothing
X_norm = normalizer.transform(X)
gamma, C, score = optimizeSVM(X_norm, y, kFolds=10)
print 'gamma=',gamma, 'C=',C, 'score=',score
clf = svm.SVC(kernel='rbf', gamma=gamma, C=C)


pathName, df = readAndReWriteCSV(baseDir, instrument, startYear=startYear, yearNum=yearNum)
print pathName
# print df.sample(3)

feed = yahoofeed.Feed()
feed.addBarsFromCSV(instrument, pathName)


class SVMStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, win=10):
        super(SVMStrategy, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        self.getBroker().setCash(initCapital)
        self.getBroker().setCommission(TradePercentage(0.003))
        self.getBroker().setAllowNegativeCash(True)
        self.getBroker().getFillStrategy().setVolumeLimit(1)
        self.getBroker().getFillStrategy().setSlippageModel(VolumeShareSlippage(priceImpact=0.0))
        self.__closeDataSeries = feed[instrument].getCloseDataSeries()
        self.df = df
        self.closeArr = []
        self.portfolios = []
        self.buys = []
        self.sells = []

        self.clf = clf
        self.X_norm = X_norm
        self.y = y
        self.actionDates = actionDates
        self.win = win
        # print 'week count:', len(y)

        self.weekCount = 1
        self.dayCount = 0
        self.errorCount = 0
        self.rightCount = 0

    def getDF(self):
        return self.df

    def getBuys(self):
        return self.buys

    def getSells(self):
        return self.sells

    def getCorrectness(self):
        return self.rightCount*1.0/(self.errorCount+self.rightCount)

    def onEnterOk(self, position):
        # execInfo = position.getEntryOrder().getExecutionInfo()
        # self.info("%s BUY %.0f shares at %.3f, commission=%.3f, PnL=%.3f" %
        #           (execInfo.getDateTime().date(), execInfo.getQuantity(), execInfo.getPrice(), execInfo.getCommission(), position.getPnL()))
        pass

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        # execInfo = position.getExitOrder().getExecutionInfo()
        # self.info("%s SELL %.0f shares at %.3f, commission=%.3f, PnL=%.3f" %
        #           (execInfo.getDateTime().date(), execInfo.getQuantity(), execInfo.getPrice(), execInfo.getCommission(), position.getPnL()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onStart(self):
        pass

    def onFinish(self, bars):
        self.df['closeArr'] = self.closeArr
        self.df['portfolio'] = self.portfolios
        # print 'dayCount=',self.dayCount, 'weekCount=',self.weekCount-1
        # print 'errorCount=',self.errorCount, 'rightCount=',self.rightCount
        pass

    def onOrderUpdated(self, order):
        execInfo = order.getExecutionInfo()
        fillDate = None
        if execInfo!=None:
            fillDate = execInfo.getDateTime().date()
            if order.getAction()==1: self.buys.append(fillDate)
            else: self.sells.append(fillDate)
        # print 'id=',order.getId(), 'state=',Order.State.toString(order.getState()), 'type=',order.getType(), \
        #     'submitAt=',order.getSubmitDateTime().date(), 'fillAt=',fillDate, \
        #     'action=',order.getAction(), 'state=',order.getState(), 'active=',order.isActive(), \
        #     'quantity=',order.getQuantity(), 'Positions=',self.getBroker().getPositions(), \
        #     'cash=', self.getBroker().getCash()

    def onBars(self, bars):
        self.closeArr.append(bars[self.__instrument].getPrice())
        self.portfolios.append(self.getBroker().getEquity())

        self.dayCount += 1
        curDate = bars[self.__instrument].getDateTime().date()
        if curDate!=self.actionDates[self.weekCount-1]: # 非每周最后一天
            return
        else:   # 每周最后一天
            if self.weekCount < self.win+1:
                self.weekCount += 1
                return
            else:
                X_train = self.X_norm[self.weekCount-self.win-1:self.weekCount-1]
                y_train = self.y[self.weekCount-self.win-1:self.weekCount-1]
                X_test = self.X_norm[self.weekCount-1]
                y_test = self.y[self.weekCount-1]
                self.clf.fit(X_train, y_train)
                result = self.clf.predict([X_test])[0]  # 为0表示跌，为1表示涨
                if result!=y_test: self.errorCount += 1 # 分类错误
                else: self.rightCount += 1 # 分类正确
                # If a position was not opened, check if we should enter a long position.
                if self.__position is None:
                    if result==1:
                        shares = int(self.getBroker().getCash() / bars[self.__instrument].getPrice())
                        hands = shares/100
                        # Enter a buy market order. The order is good till canceled.
                        self.__position = self.enterLong(self.__instrument, hands*100, False)
                # Check if we have to exit the position.
                elif not self.__position.exitActive() and result==0:
                    self.__position.exitMarket()

                self.weekCount += 1
        pass


def parameters_generator():
    win = range(6, 23)
    return itertools.product(win)


def testWithBestParameters(win=10):
    # 用最佳参数回测
    myStrategy = SVMStrategy(feed, win=win)

    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
    tradesAnalyzer = trades.Trades()
    myStrategy.attachAnalyzer(tradesAnalyzer)

    myStrategy.run()

    df = myStrategy.getDF()
    # print df[['Close', 'closeArr', 'fastSMA', 'slowSMA']].sample(5)
    buys = myStrategy.getBuys()
    sells = myStrategy.getSells()
    # print 'TRADE INFO: ', 'count=',tradesAnalyzer.getCount(), 'allProfits=',tradesAnalyzer.getAll(), 'allReturns=',tradesAnalyzer.getAllReturns()
    print "准确率: %.3f" % myStrategy.getCorrectness()
    print "总净值: %.3f" % myStrategy.getResult()
    print "总收益率: %.3f" % returnRatio(myStrategy.getResult(), C=initCapital)
    print "年化收益率: %.3f" % annualizedReturnRatioSingle(myStrategy.getResult(), C=initCapital, T=250.0*yearNum, D=250.0)

    # fig = plt.figure(figsize=(20,10))
    # ax1 = fig.add_subplot(211)
    # df[['closeArr']].plot(ax=ax1, lw=2.)
    # ax1.plot(buys, df.closeArr.ix[buys], '^', markersize=10, color='m')
    # ax1.plot(sells, df.closeArr.ix[sells], 'v', markersize=10, color='k')
    # ax2 = fig.add_subplot(212)
    # portfolio_ratio = df['portfolio']/initCapital
    # portfolio_ratio.plot(ax=ax2, lw=2.)
    # ax2.plot(buys, portfolio_ratio.ix[buys], '^', markersize=10, color='m')
    # ax2.plot(sells, portfolio_ratio.ix[sells], 'v', markersize=10, color='k')
    # # ax3 = fig.add_subplot(313)
    # # df['portfolio'].plot(ax=ax3, lw=2.)
    # # ax3.plot(buys, df['portfolio'].ix[buys], '^', markersize=10, color='m')
    # # ax3.plot(sells, df['portfolio'].ix[sells], 'v', markersize=10, color='k')
    # fig.tight_layout()
    # plt.show()


def test(isOptimize=True, win=9):
    if isOptimize:
        # 寻找最佳参数
        results = local.run(SVMStrategy, feed, parameters_generator())
        print 'Parameters:', results.getParameters(), 'Result:', results.getResult()
    else:
        # 用最佳参数回测
        testWithBestParameters(win=win)

test(isOptimize=False, win=8)