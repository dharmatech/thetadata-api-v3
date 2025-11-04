import httpx  # install via pip install httpx
import csv
import io
import pandas as pd

# https://docs.thetadata.us/operations/option_history_trade_quote.html

def option_history_trade_quote(date, symbol, expiration, other_params={}):

    
    BASE_URL = "http://localhost:25503/v3"  # all endpoints use this URL base

    # set params
    params = {
      'date': date,
      'symbol': symbol,
      'expiration': expiration,
    }

    for k, v in other_params.items():
        params[k] = v

    #
    # This is the streaming version, and will read line-by-line
    #
    url = BASE_URL + '/option/history/trade_quote'

    results = []

    with httpx.stream("GET", url, params=params, timeout=60) as response:
        response.raise_for_status()  # make sure the request worked
        for line in response.iter_lines():
            for row in csv.reader(io.StringIO(line)):
                results.append(row)

    df = pd.DataFrame(results[1:], columns=results[0])

    # df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')

    df['trade_timestamp'] = pd.to_datetime(df['trade_timestamp'], format='mixed')
    df['quote_timestamp'] = pd.to_datetime(df['quote_timestamp'], format='mixed')

    # print(df)

    return df



# every trade on 2025-10-29 for GME options expiring on 2025-10-31 with strike 24.000

# df = option_history_trade_quote('2025-10-28', 'GME', '2025-10-31', other_params={'strike':'24.000', 'right': 'CALL'})

# df = option_history_trade_quote('2025-10-28', 'GME', '2025-10-31')


# df = option_history_trade_quote('2025-10-29', 'GME', '2025-10-31', other_params={'strike':'24.000', 'right': 'CALL'})

# df.sort_values('trade_timestamp').drop(columns=['symbol', 'expiration', 'strike', 'right', 'trade_timestamp', 'quote_timestamp', 'sequence', 'ext_condition1', 'ext_condition2', 'ext_condition3', 'ext_condition4'])

# get the total of the 'size' column
# df['size'].astype(int).sum() # volume for the day

# Webull is showing strike 25 as the highest volume of all the calls.
# Let's check that.

# df = option_history_trade_quote('2025-10-29', 'GME', '2025-10-31', other_params={'strike':'25.000', 'right': 'CALL'})

# df['size'].astype(int).sum() # volume for the day


# df = option_history_trade_quote('2025-10-28', 'GME', '2025-11-07')

# df

# df.sort_values('trade_timestamp').drop(columns=['sequence', 'ext_condition1', 'ext_condition2', 'ext_condition3', 'ext_condition4'])


# df = option_history_trade_quote('2024-11-04', 'AAPL', '*')
# df = option_history_trade_quote('2024-11-04', 'AAPL', '2025-10-31')



# If I ask for yesterday, I get the data:

# http://localhost:25503/v3/option/history/trade_quote?symbol=AAPL&expiration=*&date=20251028

# If I ask for today, I get no data:

# http://localhost:25503/v3/option/history/trade_quote?symbol=AAPL&expiration=*&date=20251029