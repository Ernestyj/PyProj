import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as finance
import zipline as zp
import math
from datetime import datetime


# class DualMovingAverage(zp.TradingAlgorithm):
#     def initialize(context):
#         context.add_transform(zp.transforms.MovingAverage, 'short_mavg', ['price'], window_length=100)
#         context.add_transform(zp.transforms.MovingAverage, 'long_mavg', ['price'], window_length=400)
#         context.invested = False
#
#     def handle_data(self, data):
#         short_mavg = data['AAPL'].short_mavg['price']
#         long_mavg = data['AAPL'].long_mavg['price']
#         buy = False
#         sell = False
#         if short_mavg > long_mavg and not self.invested:
#             self.order_target('AAPL', 100)
#             self.invested = True
#             buy = True  # records that we did a buy
#         elif short_mavg < long_mavg and self.invested:
#             self.order_target('AAPL', -100)
#             self.invested = False
#             sell = True  # and note that we did sell
#         self.record(short_mavg=short_mavg, long_mavg=long_mavg, buy=buy, sell=sell)
#
# def analyze(data, perf):
#     fig = plt.figure()
#     ax1 = fig.add_subplot(211, ylabel='Price in $')
#     data['AAPL'].plot(ax=ax1, color='r', lw=2.)
#     perf[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)
#     ax1.plot(perf.ix[perf.buy].index, perf.short_mavg[perf.buy], '^', markersize=10, color='m')
#     ax1.plot(perf.ix[perf.sell].index, perf.short_mavg[perf.sell], 'v', markersize=10, color='k')
#
#     ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')
#     perf.portfolio_value.plot(ax=ax2, lw=2.)
#     ax2.plot(perf.ix[perf.buy].index, perf.portfolio_value[perf.buy], '^', markersize=10, color='m')
#     ax2.plot(perf.ix[perf.sell].index, perf.portfolio_value[perf.sell], 'v', markersize=10, color='k')
#     plt.legend(loc=0)
#     plt.gcf().set_size_inches(14, 10)



def initialize(context):
    # Register 2 histories that track daily prices, one with a 100 window and one with a 300 day window
    zp.api.add_history(100, '1d', 'price')
    zp.api.add_history(300, '1d', 'price')
    context.i = 0


def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300: return

    # Compute averages history() has to be called with the same params from above and returns a pandas dataframe.
    short_mavg = zp.api.history(100, '1d', 'price').mean()
    long_mavg = zp.api.history(300, '1d', 'price').mean()

    # Trading logic
    if short_mavg[0] > long_mavg[0]:
        # order_target orders as many shares as needed to achieve the desired number of shares.
        zp.api.order_target(zp.api.symbol('AAPL'), 100)
    elif short_mavg[0] < long_mavg[0]:
        zp.api.order_target(zp.api.symbol('AAPL'), 0)

    # Save values for later inspection
    zp.api.record(AAPL=data[zp.api.symbol('AAPL')].price, short_mavg=short_mavg[0], long_mavg=long_mavg[0])


def analyze(context, perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value in $')

    ax2 = fig.add_subplot(212)
    perf['AAPL'].plot(ax=ax2)
    perf[['short_mavg', 'long_mavg']].plot(ax=ax2)

    perf_trans = perf.ix[[t != [] for t in perf.transactions]]
    buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
    sells = perf_trans.ix[[t[0]['amount'] < 0 for t in perf_trans.transactions]]
    ax2.plot(buys.index, perf.short_mavg.ix[buys.index], '^', markersize=10, color='m')
    ax2.plot(sells.index, perf.short_mavg.ix[sells.index], 'v', markersize=10, color='k')
    ax2.set_ylabel('price in $')
    plt.legend(loc=0)
    plt.show()

if __name__ == '__main__':
    from datetime import datetime
    import pytz
    from zipline.algorithm import TradingAlgorithm
    from zipline.utils.factory import load_from_yahoo
    # Set the simulation start and end dates.
    start = datetime(2014, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc)
    # Load price data from yahoo.
    data = load_from_yahoo(stocks=['AAPL'], indexes={}, start=start, end=end)
    # Create and run the algorithm.
    algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
    results = algo.run(data)
    # Plot the portfolio and asset data.
    print results