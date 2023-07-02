import matplotlib.pyplot as plt
import csv
from datetime import date, datetime

# --- Plotting data --- #
def plotStock(symbol, file='outputs/AlpacaData.csv'):
    # Gather data
    with open(file) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        # Get dates, daily price, maS, and maL
        dates, prices, maS, maL, buy, sell = [], [], [], [], [], []
        for row in reader:
            date_str = row[0]
            date_dt = datetime.strptime(date_str[:19], '%Y-%m-%d %H:%M:%S') #date string -> datetime object
            
            # Adding data
            dates.append(date_dt)
            prices.append(float(row[1]))
            maS.append(float(row[2]))
            maL.append(float(row[3]))

            # Adding buy/sell signal if applicable
            if row[4] == 'True':
                buy.append((date_dt, float(row[1])))
            elif row[5] == 'True':
                sell.append((date_dt, float(row[1])))

            # Getting % gain
            percentGain = float(row[6])

    # Plot data
    plt.style.use('seaborn-v0_8-notebook')
    fig, ax = plt.subplots()
    ax.plot(dates, prices, c='black', alpha=0.9)
    ax.plot(dates, maS, c='red', alpha=0.3)
    ax.plot(dates, maL, c='blue', alpha=0.3)
    # buy/sell signals
    buyX, buyY = zip(*buy)
    ax.scatter(buyX, buyY, c='orange', edgecolors='black', linewidth=0.5, s=40, zorder=2)
    sellX, sellY = zip(*sell)
    ax.scatter(sellX, sellY, c='chartreuse', edgecolors='black', linewidth=0.5, s=40, zorder=2)

    # Format plot
    title = f"Daily Price of {symbol} (21/12/01 - 23/01/15)\nPercent Gain: {round(percentGain, 2)}%"
    ax.set_title(title, fontsize=20)
    ax.set_xlabel('', fontsize=16)
    fig.autofmt_xdate()
    ax.set_ylabel("Price ($)", fontsize=16)
    ax.legend(['daily price', 'short avg', 'long avg', 'buy', 'sell'], loc="upper right")

    # Show plot
    plt.show()