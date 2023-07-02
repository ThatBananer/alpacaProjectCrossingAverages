from dateutil.relativedelta import relativedelta
import config
import logging
import asyncio
import requests
import pandas as pd
import csv
from datetime import date, datetime, timedelta
from alpaca_trade_api.rest import REST  # , TimeFrame, TimeFrameUnit
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import json
import backtrader as bt
import backtrader.feeds as btfeeds

# My imports
from linked_list import LinkedList
from moving_average import MovingAverage
from plotting import plotStock

import os
import sys

# Keys
#from config.config import configApiKey, configSecretKey
import config.config as c
apiKey = c.configApiKey
secretKey = c.configSecretKey

# Imports for Paper Trading
from alpaca.trading.client import TradingClient



# ---- PAPER TRADING WITH ALGO ---- #

# paper=True enables paper trading
#trading_client = TradingClient(apiKey, secretKey, paper=True)

# Imports For Back Testing
import vectorbt as vbt
from alpaca.data import StockHistoricalDataClient, StockBarsRequest


# Functions Needed For Back Testing

# Symbol hist function
def get_symbol_history(symbol, simulationStartDate,
                       simulationEndDate):  # returns dataframe, symbol string, simulationStartDate string,
    # SimulationEndDate string
    # Converting string representation of dates to datetime objs for TimeFrame
    # datetime format
    dtStartDate = string_to_datetime(simulationStartDate)
    dtEndDate = string_to_datetime(simulationEndDate)
    # timeframe
    time_frame = get_timeframe()

    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=time_frame,
        start=dtStartDate,
        end=dtEndDate,
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


# Convert string date to datetime date
def string_to_datetime(date):
    return datetime.strptime(date, "%Y-%m-%d")


# Create timeframe object
def get_timeframe():
    tf_unit = TimeFrameUnit('Day')
    return TimeFrame(1, tf_unit)


# get new price val function
def get_new_closing_daily_price(day_iter, symbol_hist):  # day_iter int, symbol_bars df
    row = symbol_hist.iloc[day_iter]
    return row.loc['close']

# get new vwap function
def get_new_vwap(day_iter, symbol_hist):  # day_iter int, symbol_bars df
    row = symbol_hist.iloc[day_iter]
    return row.loc['vwap']


def signalVerified_vwap_vs_price(buyOrSell, day_iter, symbol_hist):  # buyOrSell String, day_iter int
    finalSingal = None
    if get_new_vwap(day_iter, symbol_hist) > get_new_closing_daily_price(day_iter, symbol_hist):
        finalSingal = "bear"
    if get_new_vwap(day_iter, symbol_hist) < get_new_closing_daily_price(day_iter, symbol_hist):
        finalSingal = "bull"
    if finalSingal == "bear" and buyOrSell == "sell" or finalSingal == "bull" and buyOrSell == "buy":
        return True
    return False


# ---- BACK TESTING DATA SET UP --- #
stock_client = StockHistoricalDataClient(apiKey, secretKey)

# ---- BACK TESTING DATA RECORDING --- #




# ---- BACK TESTING FUNCTION FOR MOVING AVERAGES --- #

def movinAvgCross(accountHoldings, maS, maL, stockSymbol, startDate, endDate, file = "outputs/AlpacaData.csv"):
    data = {
        'Date' : [],
        'DailySymbolPrice': [],
        'maSVal': [],
        'maLVal': [],
        'Buy?': [],
        'Sell?': [],
        'Percent Gain': []
    }


    hasStock = False
    day_iter = 0
    startingBalance = accountHoldings
    print(startingBalance)
    maL = MovingAverage(maL)
    maS = MovingAverage(maS)
    stockSymbol_ge_hist = get_symbol_history(stockSymbol, startDate, endDate)
    sharesOfSymbol = 0

    for index, row in stockSymbol_ge_hist.iterrows():
        signalBuy = False
        signalSell = False
        #print(index)
        newPrice = row['close']
        maL.addNewDataPoint(newPrice)
        maS.addNewDataPoint(newPrice)
        # check if moving averages were crossed
        if maL.movingAvg < maS.movingAvg and not hasStock:
            # generate buy signal
            if signalVerified_vwap_vs_price("buy", day_iter, stockSymbol_ge_hist):
                # buy
                sharesToBuy = accountHoldings // newPrice
                sharesOfSymbol += sharesToBuy
                accountHoldings -= sharesToBuy * newPrice
                hasStock = True
                #print("Stock has been bought.")
                signalBuy = True

        if maL.movingAvg > maS.movingAvg and hasStock:
            # generate sell signal
            if signalVerified_vwap_vs_price("sell", day_iter, stockSymbol_ge_hist):
                # sell
                sharesToSell = sharesOfSymbol
                sharesOfSymbol = 0
                accountHoldings = sharesToSell * newPrice
                hasStock = False
                #print("Stock has been sold.")
                signalSell = True

        day_iter += 1

        data['DailySymbolPrice'].append(newPrice)
        data['maSVal'].append(maS.movingAvg)
        data['maLVal'].append(maL.movingAvg)
        data['Date'].append(index[1])   #timestamp object saved as string
        data['Buy?'].append(signalBuy)
        data['Sell?'].append(signalSell)
        data['Percent Gain'].append((accountHoldings / startingBalance) * 100)


    print(" - - - - -  REPORT - - - - - -")
    print("startingBalance: ")
    print(startingBalance)
    print("---")
    print("accountHoldings: ")
    print(accountHoldings)
    print("---")
    print("Percent Change: ")
    print((accountHoldings / startingBalance) * 100)

    returnDF = pd.DataFrame(data)
    returnDF.to_csv(file, index=False)

    return returnDF


# Testing moving averages
movinAvgCross(100000, 5, 20, "SPY", "2021-12-01", "2023-01-15")
movinAvgCross(100000, 5, 20, "GE", "2021-12-01", "2023-01-15" )

# Testing plotting function
plotStock("GE")