import pandas as pd


def ema(data, period=0, column='Close'):
    data['ema' + str(period)] = data[column].ewm(ignore_na=False,
                                                 min_periods=period, com=period, adjust=True).mean()
    return data


def macd(data, period_long=26, period_short=12, period_signal=9, column='Close'):
    remove_cols = []
    if not 'ema' + str(period_long) in data.columns:
        data = ema(data, period_long)
        remove_cols.append('ema' + str(period_long))

    if not 'ema' + str(period_short) in data.columns:
        data = ema(data, period_short)
        remove_cols.append('ema' + str(period_short))

    data['macd_val'] = data['ema' +
                            str(period_short)] - data['ema' + str(period_long)]
    data['macd_signal_line'] = data['macd_val'].ewm(
        ignore_na=False, min_periods=0, com=period_signal, adjust=True).mean()

    # data = data.drop(remove_cols, axis=1)

    return data


def simulate_macd_avg_trading(df, ticker, short_window=7, long_window=15, gain=0.05, loss=0.05, initial_value=100):
    close_values = df[['Close']].reset_index().pivot(
        'Date', 'Ticker', 'Close')[ticker]
    trades = pd.DataFrame()
    trades['Close'] = close_values
    close_values_rolling = macd(trades)['macd_val']
    signal_values = macd(trades)['macd_signal_line']
    close_values = macd(trades)['Close']

    signal_values[short_window:]
    close_values_rolling[short_window:]

    prev_normal = signal_values[0]
    prev_rolling = close_values_rolling[0]

    wallet = initial_value
    stocks_value = 0
    diff = 0
    gain_diff = 0
    loss_diff = 0
    stocks = 0
    buys = 0
    sells = 0

    temporal_series = [0]*short_window

    sold = False

    for t in range(len(signal_values) - short_window):
        t += short_window
        current_normal = signal_values[t]
        current_closing = close_values[t]
        current_rolling = close_values_rolling[t]
        diff = (stocks*current_closing) - stocks_value

        print(stocks*current_closing, stocks_value)

        if (diff >= gain_diff or diff <= loss_diff) and stocks > 0:
            # sell
            wallet += current_closing*stocks
            stocks_value = 0
            stocks = 0
            sells += 1
            sold = True

        if prev_rolling > prev_normal and current_normal > prev_rolling:
            # buy
            if wallet//current_closing != 0:
                buys += 1
                stocks += wallet//current_closing
                wallet -= current_closing*stocks
                stocks_value = stocks*current_closing
                gain_diff = stocks_value*gain
                loss_diff = -stocks_value*loss

        if prev_normal > prev_rolling and current_normal < current_rolling and stocks > 0:
            # sell
            wallet += current_closing*stocks
            stocks_value = 0
            stocks = 0
            sells += 1
            sold = True

        if not sold:
            diff = 0
        else:
            sold = False

        temporal_series.append(diff)

        prev_normal = current_normal
        prev_rolling = current_rolling

    return wallet-initial_value, (wallet/initial_value - 1)*100, buys, sells, temporal_series
