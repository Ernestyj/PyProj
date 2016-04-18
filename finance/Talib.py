import talib

# Define the MACD function
def MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    '''
    Function to return the difference between the most recent
    MACD value and MACD signal. Positive values are long
    position entry signals

    optional args:
        fastperiod = 12
        slowperiod = 26
        signalperiod = 9

    Returns: macd - signal
    '''
    macd, signal, hist = talib.MACD(prices,
                                    fastperiod=fastperiod,
                                    slowperiod=slowperiod,
                                    signalperiod=signalperiod)
    return macd[-1] - signal[-1]