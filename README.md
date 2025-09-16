# TigerQuant Meeting Demos

## Pandas & yfinance Cheat Sheet for Quant Finance 📊

This guide covers the essential `pandas` commands for fetching, manipulating, and analyzing financial data.

### 1. Setup & Data Loading

First, import the necessary libraries and download historical stock data into a `pandas` DataFrame.

```python
import yfinance as yf
import pandas as pd
import numpy as np

# Download historical data for Apple (AAPL) and the S&P 500 ETF (SPY)
# The result is a pandas DataFrame.
data = yf.download(['AAPL', 'SPY'], start='2022-01-01')

print("Data downloaded successfully!")
```
