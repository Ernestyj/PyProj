import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as finance
import zipline as zp
import math
from datetime import datetime
from zipline import TradingAlgorithm


class MyTradingAlog(TradingAlgorithm):

    def __init__(self):
        pass

    def initialize(self):
        pass

    def handle_data(self, data):
        pass

    def analyze(self, perf):
        pass

df = pd.DataFrame({code: wsdClose['2015']})
perf = MyTradingAlog().run(df)




import zipline
from zipline import TradingAlgorithm
from zipline.api import sid, order, order_target, record, symbol, history, add_history
from zipline.api import *
from zipline.pipeline import Pipeline

code='000001.SH'
df = pd.DataFrame({code:wsdClose['2015']})
shortWin=20
longWin=40

def initialize(context):
    context.day = -1
    context.code = symbol(code)
    context.maDF = MA(df[code], shortWin=shortWin, longWin=longWin)
    context.maShort = context.maDF[str(shortWin)+'MA']
    context.maLong = context.maDF[str(longWin)+'MA']
    context.invested = False
    set_slippage(slippage.VolumeShareSlippage(volume_limit=1.0, price_impact=0.0))
    set_commission(commission.PerDollar(cost=0.003))
    pass

def handle_data(context, data):
    #print context.portfolio.cash
    context.day += 1
    i = context.day
    s = context.maShort[i]
    l = context.maLong[i]
    pres = s
    prel = l
    if i!=0:
        pres = context.maShort[i-1]
        prel = context.maLong[i-1]
    if i>=longWin-1:
        if s>l and pres<=prel and not context.invested:
            order_percent(symbol(code), 1.0)
            context.invested = True
        elif s<l and context.invested:
            order_percent(symbol(code), -1.0)
            context.invested = False
    record(maShort=s, maLong=l)
    pass

def analyze(context, perf):
    perf_trans = perf.ix[[t!=[] for t in perf.transactions]]
    buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
    sells = perf_trans.ix[[t[0]['amount'] < 0 for t in perf_trans.transactions]]

    fig = plt.figure(figsize=(20,15))
    ax1 = fig.add_subplot(311)
    #data['AAPL'].plot(ax=ax1, color='r', lw=2.)
    perf[['maShort', 'maLong']].plot(ax=ax1, lw=2.)
    ax1.plot(buys.index, perf.maShort.ix[buys.index], '^', markersize=10, color='m')
    ax1.plot(sells.index, perf.maLong.ix[sells.index], 'v', markersize=10, color='k')

    ax2 = fig.add_subplot(312)
    portfolio_ratio = perf.portfolio_value/100000.0
    portfolio_ratio.plot(ax=ax2, lw=2.)
    ax2.plot(buys.index, portfolio_ratio.ix[buys.index], '^', markersize=10, color='m')
    ax2.plot(sells.index, portfolio_ratio.ix[sells.index], 'v', markersize=10, color='k')

#     ax3 = fig.add_subplot(313)
#     perf.portfolio_value.plot(ax=ax3, lw=2.)
#     ax3.plot(buys.index, perf.portfolio_value.ix[buys.index], '^', markersize=10, color='m')
#     ax3.plot(sells.index, perf.portfolio_value.ix[sells.index], 'v', markersize=10, color='k')
    pass

algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
algo._analyze = analyze
perf = algo.run(df)

perf_trans = perf.ix[[t!=[] for t in perf.transactions]]
buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
sells = perf_trans.ix[[t[0]['amount'] < 0 for t in perf_trans.transactions]]
investDays = validInvestDays(buys, sells, perf)
print investDays
cashes = perf.portfolio_value.ix[sells.index]
returnRatArr = returnRatioArr(cashes.values)
final_return_ratio = returnRatio(perf.portfolio_value[-1])
print '总收益率：', final_return_ratio
print '年化收益率：', annualizedReturnRatio([final_return_ratio], T=investDays, D=250.0)



