from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

import datetime
import pandas as pd
import numpy as np

def get_sharpe(df):
    adj_close = df[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close')
    daily_pct_change = adj_close.pct_change()
    daily_pct_change.fillna(0, inplace=True)
    sharpe = daily_pct_change.mean()/daily_pct_change.std()
    return sharpe

def get_annual_sharpe(df, years=1):
    sharpe = get_sharpe(df)
    return sharpe * ((years*252)**0.5) # Square root of 252 commercial days

def get_return_by_ticker(df):
    adj_close = df[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close')
    daily_log_returns = np.log(adj_close.pct_change()+1)
    daily_log_returns.fillna(0, inplace=True)
    return_series = daily_log_returns.sum()
    return return_series

def get_positive_return_tickers_series(df):
    return_series = get_return_by_ticker(df)
    return return_series[return_series > 0].index.values

def filter_positive_returns(df):
    return df.loc[ get_positive_return_tickers_series(df) , : ]

def get_correlation(df):
    adj_close = df[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close')
    return adj_close.corr()