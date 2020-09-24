import time
import datetime
import numpy as np
from ndfinance.brokers.base.order import *
from ndfinance.brokers.base.asset import *
from ndfinance.brokers.base.data_provider import *
from ndfinance.brokers.base.position import *
from ndfinance.brokers.base.withdraw import WithDrawConfig, WithDrawTypes

class Config :
    name="config"


class Types:
    name="types"


class Broker:
    def __init__(self, data_provider, withdraw_config):
        self.data_provider = data_provider
        self.indexer = self.data_provider.indexer
        self.withdraw_config = withdraw_config

    def order(self, order):
        raise NotImplementedError

    def withdraw(self):
        raise NotImplementedError


class TimeFrames:
    minute = 60
    second = 1
    hour = minute * 60
    day = hour * 24
    week = day * 7


class TimeIndexer(object):
    def __init__(self, timestamp_lst, from_timestamp=-np.inf, to_timestamp=np.inf):
        self.timestamp = None

        if isinstance(to_timestamp, str):
            to_timestamp = time.mktime(datetime.datetime.strptime(to_timestamp, "%Y-%m-%d").timetuple())

        if isinstance(from_timestamp, str):
            from_timestamp = time.mktime(datetime.datetime.strptime(from_timestamp, "%Y-%m-%d").timetuple())

        self.timestamp_lst = timestamp_lst[np.where(
            (from_timestamp <= timestamp_lst) & (timestamp_lst <= to_timestamp))[0]]

        self.idx = -1
        self.lastidx = len(self.timestamp_lst)
        self.first_timestamp = self.timestamp_lst[0]
        self.last_timestamp = self.timestamp_lst[-1]
        self.move()

    def move(self):
        self.idx += 1
        self.timestamp = self.timestamp_lst[self.idx]

    def is_done(self):
        return self.idx == self.lastidx

    @property
    def datetime(self):
        return datetime.datetime.fromtimestamp(self.timestamp)