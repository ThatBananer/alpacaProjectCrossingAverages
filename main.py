import vectorbt as vbt

from dateutil.relativedelta import relativedelta
import config
import logging
import asyncio
import requests
import pandas as pd
from datetime import date, datetime
#from ta.volatility import BollingerBands
#from ta.momentum import RSIIndicator
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





# Imports for Back Testing


from alpaca.data import StockHistoricalDataClient, StockBarsRequest
from alpaca.data import StockHistoricalDataClient


# ---- BACK TESTING --- #
simulationStartDate = "2023-01-01"
simulationEndDate = "2023-05-15"



stock_client = StockHistoricalDataClient(apiKey,  secretKey)


while 1 == 1:
    # add new vals to moving average
    # check if moving avergaes were crossed
        #generate buy sell signal
    ## verify possible singal
        #execute based on signal
    #break if no more data
    break




def get_day_by_day_price(symbol): # returns dataframe
    request_params = StockBarsRequest(
                        symbol_or_symbols=[symbol],
                        timeframe=TimeFrame.Day,
                        start=simulationStartDate,
                        end= simulationEndDate,
                    )
    symbol_bars = stock_client.get_stock_bars(request_params)
    return symbol_bars.df
# Expected output format of get_day_by_day_price()
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



# ---- Linked List Class ---- #
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def prepend(self, data):
        new_node = Node(data)
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

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next