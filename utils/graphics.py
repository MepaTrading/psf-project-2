import plotly.graph_objects as go
import datetime
import matplotlib.pyplot as plt
import numpy as np

def candlestick_from_all_data(df, ticker):
    open_values = df[['Open']].reset_index().pivot('Date', 'Ticker', 'Open')
    high_values = df[['High']].reset_index().pivot('Date', 'Ticker', 'High')
    low_values = df[['Low']].reset_index().pivot('Date', 'Ticker', 'Low')
    close_values = df[['Close']].reset_index().pivot('Date', 'Ticker', 'Close')

    dates = close_values[ticker].index.values
    dates_list = [datetime.datetime.utcfromtimestamp(each.tolist()/1e9) for each in close_values[ticker].index.values]
    dates_list = [each.strftime("%Y-%m-%d") for each in dates_list]

    cs = go.Candlestick(x=dates_list, open=open_values[ticker], high=high_values[ticker], low=low_values[ticker], close=close_values[ticker])
    fig = go.Figure(data=cs)

    return fig

def volume_for_all_data(df, ticker):
    volume_values = df[['Volume']].reset_index().pivot('Date', 'Ticker', 'Volume')
    volume_list = volume_values[ticker].values
    
    dates_list = np.linspace(1, len(volume_values[ticker].index.values), len(volume_values[ticker].index.values))

    volume = plt.plot(dates_list, volume_list)

    return volume

def monthly_return_for_all_data(df, ticker):
    adj_close = df[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close').asfreq("M", method="bfill").pct_change().fillna(0)
    return_df = adj_close[ticker].values

    dates_list = np.linspace(1, len(adj_close[ticker].index.values), len(adj_close[ticker].index.values))

    ret = plt.plot(dates_list, return_df)

    return ret

    