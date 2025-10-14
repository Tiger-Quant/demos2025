# EMA_Crossover_Test.py
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Ticker symbol and data download
data_to_use = 'SPY'
data = yf.download(data_to_use, start='2022-01-01')
data.columns = data.columns.droplevel(1)  # drop MultiIndex if exists

def calculate_returns(quantity, data): #reused from other demo
    total_profit = 0
    total_money_invested = 0

    buy_signal = (data['Signal'] == 1.0)
    sell_signal = (data['Signal'] == -1.0)

    for buy_time, buy_row in data[buy_signal].iterrows():
        buy_price = buy_row['Close']
        sell_trades = data[sell_signal & (data.index > buy_time)]

        if not sell_trades.empty:
            sell_price = sell_trades.iloc[0]['Close']
            profit = quantity * (sell_price - buy_price)
            money_invested = quantity * buy_price
            print(f"Bought {quantity} share(s) at ${buy_price:.2f}. "
                  f"Sold {quantity} share(s) at ${sell_price:.2f}, Profit: ${profit:.2f}")

            total_profit += profit
            total_money_invested += money_invested
        else:
            print(f"Would buy {quantity} share(s) at ${buy_price:.2f}, but no sell signal found.")

    roi = (total_profit / total_money_invested) if total_money_invested != 0 else 0
    print(f"\nTotal Profit: ${total_profit:.2f}, "
          f"Money Invested: ${total_money_invested:.2f}, "
          f"Return on Investment: {roi*100:.2f}%")
    return total_profit, roi


def plot_data(data, data_name=data_to_use): #reused from other demo
    plt.figure(figsize=(12,6))
    plt.plot(data['Close'], label=f"{data_name} Close Price", alpha=0.5)
    plt.title(f"{data_name} Closing Prices Since 2022")
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')

# Calculate 12/26 EMAs
data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()
data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()

# Generate signals
data['Position'] = np.where(data['EMA12'] > data['EMA26'], 1, 0)
data['Signal'] = data['Position'].diff()

# Plotting
plot_data(data)
plt.plot(data['EMA12'], label='12-Day EMA', linestyle='--')
plt.plot(data['EMA26'], label='26-Day EMA', linestyle='-.')

# Highlight buy/sell signals
buy_signal = data['Signal'] == 1.0
sell_signal = data['Signal'] == -1.0
plt.scatter(data.index[buy_signal], data['Close'][buy_signal], label='Buy Signal', marker='^', color='green', s=100)
plt.scatter(data.index[sell_signal], data['Close'][sell_signal], label='Sell Signal', marker='v', color='red', s=100)

plt.legend()
plt.show()

calculate_returns(1, data)