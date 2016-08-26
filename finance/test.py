#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

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


pathName, df = readAndReWriteCSV(baseDir, instrument, '2010-06-01', '2013-06-06')