# -*- coding: utf-8 -*-
from datetime import datetime


class CommonUtils():
    def __init__(self):
        pass

    @staticmethod
    def datetime2str(ts, fmt="%Y-%m-%d %H:%M:%S"):
        return datetime.strftime(ts, fmt)

    @staticmethod
    def str2datetime(ts, fmt="%Y-%m-%d %H:%M:%S"):
        return datetime.strptime(ts, fmt)

    @staticmethod
    def unixtime2ts(unixtime, use_timezone='US/Pacific'):
        if isinstance(unixtime, str) or isinstance(unixtime, unicode):
            unixtime = int(unixtime)
        return datetime.fromtimestamp(unixtime, timezone(use_timezone)).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def ts2unixtime(ts, fmt="%Y-%m-%d %H:%M:%S", use_timezone='US/Pacific'):
        if isinstance(ts, str):
            ts = datetime.strptime(ts, fmt)
        if not isinstance(ts, datetime):
            raise TypeError
        local_ts = timezone(use_timezone).localize(ts)
        unix_ts = calendar.timegm(local_ts.utctimetuple())
        return unix_ts