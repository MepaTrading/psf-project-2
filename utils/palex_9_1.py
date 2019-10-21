def simulate_palex_9_1(df, ticker, gain=0.05, down_len=5, initial_value=100):
    close_values = df[['Close']].reset_index().pivot('Date', 'Ticker', 'Close')[ticker]
    close_values_rolling = close_values.ewm(span=9, adjust=False).mean()

    open_values = df[['Open']].reset_index().pivot('Date', 'Ticker', 'Open')[ticker]

    wallet = initial_value
    stocks = 0
    buys = 0
    sells = 0
    before_trade_wallet = wallet
    down_candles = 0

    start = 0
    stop_loss = 0
    stop_gain = 0

    temporal_series = [0]*9

    sold = False
    is_setup = False

    prev_rolling = None
    current_rolling = None

    for t in range(len(close_values) - 9):
        t+=9
        current_rolling = close_values_rolling[t]

        if prev_rolling is None:
            prev_rolling = current_rolling
            continue

        diff = (stocks*close_values[t]) - (before_trade_wallet)

        if current_rolling > prev_rolling:
            # Positive candle
            if down_candles >= down_len:
                # Setup 9.1
                is_setup = True
                start = close_values[t]
                stop_loss = open_values[t]
        else:
            # Negative candle
            is_setup = False
            down_candles+=1

        if is_setup and close_values[t] >= start:
            # buy
            if wallet//close_values[t] > 0:
                stocks = wallet//close_values[t]
                before_trade_wallet = stocks * close_values[t]
                wallet -= before_trade_wallet
                stop_gain = before_trade_wallet + (before_trade_wallet*gain)
                buys+=1

        if stocks > 0:
            if (stocks*close_values[t]) >= stop_gain or close_values[t] <= stop_loss:
                # sell to win
                sold = True
                wallet += stocks*close_values[t]
                is_setup = False
                stocks = 0
                sells+=1

        if not sold:
            diff=0
        else:
            sold = False

        temporal_series.append(diff)

        prev_rolling = current_rolling

    return wallet-initial_value, (wallet/initial_value - 1)*100, buys, sells, temporal_series