#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pyalgotrade import strategy, plotter
from pyalgotrade.broker.backtesting import TradePercentage, Broker
from pyalgotrade.broker import Order
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.broker.slippage import NoSlippage, VolumeShareSlippage
from pyalgotrade.stratanalyzer import returns, trades
from pyalgotrade.optimizer import server, local
import itertools

from sklearn import preprocessing, svm, cross_validation, metrics, pipeline, grid_search
from scipy.stats import sem

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

usecols = [0, 2,11,24,26,29,30]
usecols = [0, 1,2,3,4,5,6]
def readWSDIndexFile(baseDir, stockCode, startYear, yearNum=1):
    # 解析日期
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d').date()

    df = 0
    for i in range(yearNum):
        tempDF = pd.read_csv(baseDir+'I'+stockCode+'/wsd_'+stockCode+'_'+str(startYear+i)+'.csv',
                                index_col=0, sep=',', parse_dates=True, date_parser=dateparse, usecols=usecols)
        if i==0: df = tempDF
        else: df = df.append(tempDF)
    return df

def prepareData(df, dfi, win=5):
    # 跳过第一个值
    opens = [0]; openArr = []
    highs = [0]; highArr = []
    lows = [0]; lowArr = []
    volumes = [0]; volumeArr = []
    changes = [0]; changeArr = []
    changePcts = [0]; changePctArr = []
    averages = [0]; averageArr = []
    turns = [0]; turnArr = []
    rs = [0]; closeArr = []
    lastRs = [0]
    weekAgoRs = [0]
    amts = [0]; amtArr = []
    lastAmts = [0]

    techs = []
    techArr = []

    upOrDowns = [0]  # 为0表示跌，为1表示涨
    actionDates = [0]
    # fourWeekAvgAmts = [0];#暂不加入计算
    count = 0
    for i in range(len(df)):
        if count<win:
            openArr.append(df['Open'][i])
            highArr.append(df['High'][i])
            lowArr.append(df['Low'][i])
            volumeArr.append(df['Volume'][i])
            changeArr.append(df['Chg'][i])
            changePctArr.append(df['Chg Pct'][i])
            averageArr.append(df['Avg'][i])
            turnArr.append(df['Turn'][i])
            closeArr.append(df['Close'][i])
            amtArr.append(df['Amount'][i])
            techArr.append(dfi.iloc[i].values)
            count += 1
        if count==win:
            opens.append(np.mean(openArr))
            highs.append(np.mean(highArr))
            lows.append(np.mean(lowArr))
            volumes.append(np.mean(volumeArr))
            changes.append(np.mean(changeArr))
            changePcts.append(np.mean(changePctArr))
            averages.append(np.mean(averageArr))
            turns.append(np.mean(turnArr))
            rs.append((closeArr[-1] - closeArr[0]) / closeArr[0])
            lastRs.append(rs[-2])
            weekAgoRs.append(lastRs[-2])
            amts.append(np.mean(amtArr))
            lastAmts.append(amts[-2])
            techs.append(np.mean(techArr, axis=0))
            upOrDown = -1
            if rs[-1] > 0.0: upOrDown = 1
            elif rs[-1] == 0.0: upOrDown = upOrDowns[-1]  # 无涨跌时，按前周的涨跌情况
            else: upOrDown = -1
            upOrDowns.append(upOrDown)
            actionDates.append(df.index[i].date())
            del openArr[:]; del highArr[:]; del lowArr[:]; del volumeArr[:]; del changeArr[:]; del changePctArr[:];
            del averageArr[:]; del turnArr[:]; del closeArr[:]; del amtArr[:]
            del techArr[:]
            count = 0
    if count!=0: # 处理剩余数据
        opens.append(np.mean(openArr))
        highs.append(np.mean(highArr))
        lows.append(np.mean(lowArr))
        volumes.append(np.mean(volumeArr))
        changes.append(np.mean(changeArr))
        changePcts.append(np.mean(changePctArr))
        averages.append(np.mean(averageArr))
        turns.append(np.mean(turnArr))
        rs.append((closeArr[-1] - closeArr[0]) / closeArr[0])
        lastRs.append(rs[-2])
        weekAgoRs.append(lastRs[-2])
        amts.append(np.mean(amtArr))
        lastAmts.append(amts[-2])
        techs.append(np.mean(techArr, axis=0))
        upOrDown = -1
        if rs[-1] > 0.0: upOrDown = 1
        elif rs[-1] == 0.0: upOrDown = upOrDowns[-1]  # 无涨跌时，按前周的涨跌情况
        else: upOrDown = -1
        upOrDowns.append(upOrDown)
        actionDates.append(df.index[i].date())

    tempX = np.column_stack((changes[1:], changePcts[1:], volumes[1:], amts[1:], turns[1:]))
    X = np.hstack((tempX, techs))
    y = upOrDowns[2:]  # 涨跌数组向后移一位,表当前周数据预测下一周涨跌
    y.append(upOrDowns[-1])  # 涨跌数组最后一位按前一位数据补上
    return X, y, actionDates[1:]

def optimizeSVM(X_norm, y, kFolds=10):
    clf = pipeline.Pipeline([
        ('svc', svm.SVC(kernel='rbf')),
    ])
    # grid search 多参数优化
    parameters = {
        'svc__gamma': np.logspace(-3, 11, 8, base=2),
        'svc__C': np.logspace(-3, 15, 10, base=2),
    }
    gs = grid_search.GridSearchCV(clf, parameters, verbose=1, refit=False, cv=kFolds)
    gs.fit(X_norm, y)
    return gs.best_params_['svc__gamma'], gs.best_params_['svc__C'], gs.best_score_


class SVMStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, clf, df, X_norm, y, actionDates, initCapital=100000, win=10):
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
        self.predictions = []
        self.win = win
        # print 'week count:', len(y)

        self.segmentCount = 1
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

    def getPredictions(self):
        return self.predictions

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
            if order.getAction()==1: self.buys.append([fillDate, execInfo.getPrice(), execInfo.getQuantity()])
            else: self.sells.append([fillDate, execInfo.getPrice(), execInfo.getQuantity()])
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
        if curDate!=self.actionDates[self.segmentCount-1]: # 非区间最后一天
            return
        else:   # 区间最后一天
            if self.segmentCount < self.win+1:
                self.segmentCount += 1
                return
            else:
                X_train = self.X_norm[self.segmentCount - self.win - 1:self.segmentCount - 1]
                y_train = self.y[self.segmentCount - self.win - 1:self.segmentCount - 1]
                X_test = self.X_norm[self.segmentCount - 1]
                y_test = self.y[self.segmentCount - 1]
                self.clf.fit(X_train, y_train)
                result = self.clf.predict([X_test])[0]  # 为-1表示跌，为1表示涨
                self.predictions.append(result)
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
                elif not self.__position.exitActive() and result==-1:
                    self.__position.exitMarket()

                self.segmentCount += 1
        pass

'''
计算收益率
'''
def returnRatio(V, C=100000.0):
    return V/C-1.0

'''
计算年化收益率(单期)
'''
def annualizedReturnRatioSingle(portfolio, C=100000.0, T=250.0, D=250.0):
    import math
    return math.pow(portfolio/C, D/T) - 1


def parameters_generator():
    win = range(13, 23)
    return itertools.product(win)



def day_svm_backtest(baseDir, instrument, initCapital=100000, startYear=2014, yearNum=2, winK=15, win=10):
    df = readWSDFile(baseDir, instrument, startYear, yearNum)
    dfi = readWSDIndexFile(baseDir, instrument, startYear, yearNum)

    X, y, actionDates = prepareData(df, dfi, win=winK)
    normalizer = preprocessing.Normalizer().fit(X)  # fit does nothing
    X_norm = normalizer.transform(X)
    gamma, C, score = optimizeSVM(X_norm, y, kFolds=10);
    clf = svm.SVC(kernel='rbf', gamma=gamma, C=C)

    pathName, df = readAndReWriteCSV(baseDir, instrument, startYear=startYear, yearNum=yearNum)
    # print pathName

    feed = yahoofeed.Feed()
    feed.addBarsFromCSV(instrument, pathName)

    myStrategy = SVMStrategy(feed, instrument, clf, df, X_norm, y, actionDates, initCapital=initCapital, win=win)
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
    tradesAnalyzer = trades.Trades()
    myStrategy.attachAnalyzer(tradesAnalyzer)
    myStrategy.run()

    res_df = myStrategy.getDF()
    # print res_df[['Close', 'closeArr', 'fastSMA', 'slowSMA']].sample(5)
    buys = myStrategy.getBuys()
    sells = myStrategy.getSells()
    # print myStrategy.getPredictions();
    dates = res_df.index.date.tolist()
    dates_ = [date.strftime('%Y-%m-%d') for date in dates]
    print dates_
    print res_df['closeArr'].values.tolist()
    buys_ = [[buy[0].strftime('%Y-%m-%d'), buy[1], buy[2]] for buy in buys]
    sells_ = [[sell[0].strftime('%Y-%m-%d'), sell[1], sell[2]] for sell in sells]
    actionDates_ = [date.strftime('%Y-%m-%d') for date in actionDates]
    print buys_; print sells_; print actionDates_
    print res_df['portfolio'].values.tolist()
    # print 'TRADE INFO: ', 'count=',tradesAnalyzer.getCount(), 'allProfits=',tradesAnalyzer.getAll(), 'allReturns=',tradesAnalyzer.getAllReturns()
    print myStrategy.getCorrectness()
    print myStrategy.getResult()
    print returnRatio(myStrategy.getResult(), C=initCapital)
    print annualizedReturnRatioSingle(myStrategy.getResult(), C=initCapital, T=250.0 * yearNum, D=250.0)

import sys   ##加载sys这个模块。
# for i in range(len(sys.argv)): print "%d parameter: %s" % (i, sys.argv[i])

import time
start = time.time()

baseDir = 'E:\\Downloads\\Data\\'
# baseDir = '/Users/eugene/Downloads/data/'
instruments = ['000300.SH', '000016.SH', '000905.SH', '002047.SZ', '600015.SH', '600674.SH']
instrument = instruments[0]
initCapital = 100000000
startYear = 2014
yearNum = 2
winK = 15
win = 10

# day_svm_backtest(baseDir=baseDir, instrument=instrument, initCapital=100000000,
#                  startYear=2014, yearNum=2, winK=15, win=10)
# baseDir = str(sys.argv[1])
# instrument = str(sys.argv[2])
# initCapital = int(sys.argv[3])
# startYear = int(sys.argv[4])
# yearNum = int(sys.argv[5])
# winK = int(sys.argv[6])
# win = int(sys.argv[7])

# print baseDir, instrument, initCapital, startYear, yearNum, winK, win
day_svm_backtest(baseDir=baseDir, instrument=instrument, initCapital=initCapital,
                 startYear=startYear, yearNum=yearNum, winK=winK, win=win)

end = time.time()
print 'time:',end-start