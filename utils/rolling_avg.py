def simulate_rolling_avg_trading(df, ticker, rolling_window=7, gain=0.05, loss=0.05, initial_value=100):
    close_values = df[['Close']].reset_index().pivot('Date', 'Ticker', 'Close')[ticker]
    close_values_rolling = close_values.rolling(rolling_window).mean()

    close_values[rolling_window:]
    close_values_rolling[rolling_window:]

    prev_normal = close_values[0]
    prev_rolling = close_values_rolling[0]

    wallet = initial_value
    stocks_value = 0
    diff = 0
    gain_diff = 0
    loss_diff = 0
    stocks = 0
    buys = 0
    sells = 0
    before_trade_wallet = wallet

    temporal_series = [0]*rolling_window

    sold = False

    for t in range(len(close_values) - rolling_window):
        t+=rolling_window
        current_normal = close_values[t]
        current_rolling = close_values_rolling[t]
        diff = (stocks*current_normal) - stocks_value

        if (diff >= gain_diff or diff <= loss_diff) and stocks > 0:
            #sell
            wallet += current_normal*stocks
            stocks_value = 0
            stocks = 0
            sells+=1
            sold=True

        if prev_rolling > prev_normal and current_normal > prev_rolling:
            # buy
            if wallet//current_normal != 0:
                buys+=1
                stocks+=wallet//current_normal
                wallet -= current_normal*stocks
                stocks_value = stocks*current_normal
                gain_diff = stocks_value*gain
                loss_diff = -stocks_value*loss

        
        if prev_normal > prev_rolling and current_normal < current_rolling and stocks > 0:
            # sell
            wallet += current_normal*stocks
            stocks_value = 0
            stocks = 0
            sells+=1
            sold=True

        if not sold:
            diff=0
        else:
            sold = False

        temporal_series.append(diff)

        prev_normal = current_normal
        prev_rolling = current_rolling

    return wallet-initial_value, (wallet/initial_value - 1)*100, buys, sells, temporal_series