import vectorbt as vbt
import alpaca_trade_api

# Keys
vbt.settings.data['alpaca']['key_id'] = 'key'
vbt.settings.data['alpaca']['secret_key'] = 'secret key'

# Retrieving data from 30 days ago UTC
alpacadata = vbt.AlpacaData.download(symbols='AAPL', start='30 days ago UTC', end='1 day ago UTC', timeframe='1h')

# Simple Moving Average Crossover
fast_ma = vbt.MA.run(alpacadata, 10, short_name='fast')
slow_ma = vbt.MA.run(alpacadata, 20, short_name='slow')

entries = fast_ma.ma_crossed_above(slow_ma)
#print(entries)