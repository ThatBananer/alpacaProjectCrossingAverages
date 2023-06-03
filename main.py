import vectorbt as vbt

from dateutil.relativedelta import relativedelta
import config
import logging
import asyncio
import requests
import pandas as pd
from datetime import date, datetime
# from ta.volatility import BollingerBands
# from ta.momentum import RSIIndicator
from alpaca_trade_api.rest import REST, TimeFrame
import json
import backtrader as bt
import backtrader.feeds as btfeeds

apiKey = "PlaceHolder"
secretKey = "PlaceHolder"

# Imports for Paper Trading

from alpaca.trading.client import TradingClient

# ---- PAPER TRADING WITH ALGO ---- #

# paper=True enables paper trading
trading_client = TradingClient(apiKey, secretKey, paper=True)

# Imports For Back Testing

from alpaca.data import StockHistoricalDataClient, StockBarsRequest
from alpaca.data import StockHistoricalDataClient

# Functions Needed For Back Testing

# Symbol hist function
def get_symbol_history(symbol, simulationStartDate,
                       simulationEndDate):  # returns dataframe, symbol string, simulationStartDate string, SimulationEndDate string
    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame.Day,
        start=simulationStartDate,
        end=simulationEndDate,
    )
    symbol_bars = stock_client.get_stock_bars(request_params)
    return symbol_bars.df

# Expected output format of get_symbol_history(symbol)
"""
symbol  		timestamp                		open  	    high	    low 	    close	    volume		    trade_count	    vwap
BTC/USD 	    2022-09-01 05:00:00+00:00   	20049.0 	20285.0	    19555.0 	20160.0 	2396.3504   	18060.0		    19920.278135
        		2022-09-02 05:00:00+00:00   	20159.0 	20438.0 	19746.0 	19924.0 	1688.0641   	16730.0 		20045.987764
        		2022-09-03 05:00:00+00:00   	19924.0 	19963.0 	19661.0 	19802.0 	624.1013    	9853.0  		19794.111057
		        2022-09-04 05:00:00+00:00   	19801.0 	20060.0 	19599.0 	19892.0 	1361.6668   	8489.0  		19885.445568
		        2022-09-05 05:00:00+00:00   	19892.0 	20173.0 	19640.0 	19762.0 	2105.0539   	11900.0 		19814.853546
		        2022-09-06 05:00:00+00:00   	19763.0 	20025.0 	18539.0 	18720.0 	3291.1657   	19591.0 		19272.505607
		        2022-09-07 05:00:00+00:00   	18723.0 	19459.0 	18678.0 	19351.0 	2259.2351   	16204.0 		19123.487500
"""


# get new price val function
def get_new_closing_daily_price(day_iter, symbol_hist):  # day_iter int, symbol_bars df
    return symbol_hist.loc[day_iter, 'close']


# ---- BACK TESTING --- #
simulationStartDate = "2023-01-01"
simulationEndDate = "2023-05-15"

generalElectricCoSymbol = "GE"

stock_client = StockHistoricalDataClient(apiKey, secretKey)

ge_hist = get_symbol_history(generalElectricCoSymbol, simulationStartDate, simulationEndDate)

while 1 == 1:
    day_iter = 0
    # get new price val
    newPrice = get_new_closing_daily_price(day_iter, ge_hist)
    # add new vals to moving average
    # check if moving avergaes were crossed
    # generate buy sell signal
    ## verify possible singal
    # execute based on signal
    # break if no more data
    day_iter = + 1
    break


# ---- Linked List Class ---- #
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    # append means add to tail
    def newTail(self, data):
        new_node = Node(data)
        self.length += 1
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    # prepend means add to head
    def newHead(self, data):
        new_node = Node(data)
        self.length += 1
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    def delete_head(self):
        if self.head is None:
            return
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
        self.length -= 1


    def delete_tail(self):
        if self.tail is None:
            return
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            current = self.head
            while current.next != self.tail:
                current = current.next
            current.next = None
            self.tail = current
        self.length -= 1


    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next


class MovingAverage:
    def __init__(self, time_period_days):
        self.time_period_days = time_period_days
        self.linked_list = self.__createLinkedList(self)
        self.movingAvg = 0
        self.movingAvgSum = 0


    # ---- public methods ---- #

    # get moving avg
    def getMA(self):
        if self.movingAvg is 0:
            print("MA is 0 in getMA")
            return 0
        return self.movingAvg

    # add new day data point
    # needs to: get find new avg, delete oldest val if at limit, add newest val to front
    def addNewDataPoint(self, newVal):
        self.__calcNewMA(newVal)


    # ---- private methods ---- #

    # calc new avg
    def __calcNewMA(self, newVal):
        self.linked_list.newHead(newVal)
        self.movingAvgSum =+ newVal
        if self.linked_list.length == self.time_period_days:
            self.movingAvgSum =- self.linked_list.tail
            self.linked_list.delete_tail()

        if self.movingAvg == 0:
            self.movingAvg = newVal
        else:
            self.movingAvg = self.movingAvgSum / self.linked_list.length

    # linked list creation
    def __createLinkedList(self):
        return LinkedList()

    # ...
