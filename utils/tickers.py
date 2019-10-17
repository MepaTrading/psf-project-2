from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

import datetime
import pandas as pd

def get_tickers(tickers, startdate=(datetime.datetime.today() - datetime.timedelta(days=365*2)), enddate=datetime.datetime.today()):
  def data(ticker):
    data = pdr.get_data_yahoo(ticker, start=startdate, end=enddate)
    return data
  datas = map (data, tickers)
  return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))

def daily_adj_close(all_data):
    return all_data[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close')