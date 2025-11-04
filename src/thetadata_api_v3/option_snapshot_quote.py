import httpx  # install via pip install httpx
import csv
import sys
import io
import pandas as pd
from datetime import datetime


def option_snapshot_quote(symbol, expiration, other_params={}):

    BASE_URL = "http://localhost:25503/v3"  # all endpoints use this URL base

    params = {
        'symbol': symbol,
        'expiration': expiration,
    }

    for k, v in other_params.items():
        params[k] = v

    # Weekend Check (Sat/Sun)
    now = datetime.now()

    if now.weekday() >= 5: # 5=Sat, 6=Sun
        print("Market is Closed snapshots may not work")
        sys.exit(0)

    #
    # This is the streaming version, and will read line-by-line
    #
    url = BASE_URL + '/option/snapshot/quote'

    results = []

    with httpx.stream("GET", url, params=params, timeout=60) as response:
        response.raise_for_status()  # make sure the request worked
        for line in response.iter_lines():
            for row in csv.reader(io.StringIO(line)):
                results.append(row)
    
    df = pd.DataFrame(results[1:], columns=results[0])

    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
    df['strike'] = pd.to_numeric(df['strike'])
    df['bid'] = pd.to_numeric(df['bid'])
    
    # Calculate days till expiration (dte)
    df['expiration_date'] = pd.to_datetime(df['expiration'], format='%Y-%m-%d')
    today = pd.Timestamp.now().normalize()  # Get today's date at midnight
    df['dte'] = (df['expiration_date'] - today).dt.days
    
    # Drop the temporary expiration_date column
    df = df.drop('expiration_date', axis=1)

    return df


def calculate_premium_metrics(df):
    # Calculate days till expiration (dte)
    df['expiration_date'] = pd.to_datetime(df['expiration'], format='%Y-%m-%d')
    today = pd.Timestamp.now().normalize()  # Get today's date at midnight
    df['dte'] = (df['expiration_date'] - today).dt.days
    
    # Drop the temporary expiration_date column
    df = df.drop('expiration_date', axis=1)
    
    # Calculate premium per dte
    df['premium_per_dte'] = df['bid'] * 100 / df['dte']
    df['premium_per_dte'] = df['premium_per_dte'].round(2)
    
    # Calculate premium per day per collateral
    df['premium_per_day_per_collateral'] = df['premium_per_dte'] / (df['strike'] * 100)
    
    # Calculate ppdpc_pct
    df['ppdpc_pct'] = df['premium_per_day_per_collateral'] * 100
    df['ppdpc_pct'] = df['ppdpc_pct'].round(4)
    
    return df


__all__ = ['option_snapshot_quote', 'calculate_premium_metrics']

# df = option_snapshot_quote('GME', expiration='2025-10-31')

# df = option_snapshot_quote('GME', expiration='2025-10-31', other_params={'strike':'24.000'})

# df

# >>> df = option_snapshot_quote('GME', expiration='2025-10-31')
# >>> df
#                  timestamp symbol  expiration  strike right bid_size bid_exchange   bid bid_condition ask_size ask_exchange    ask ask_condition
# 0  2025-10-29 15:59:59.446    GME  2025-10-31  32.000   PUT      157            4  8.35            50      208           65   9.25            50
# 1  2025-10-29 09:31:28.370    GME  2025-10-31  16.000   PUT        0           76  0.00            50       10            7   0.01            50
# 2  2025-10-29 15:59:59.448    GME  2025-10-31  16.000  CALL      210           65  5.30            50      210           65   8.40            50
# 3  2025-10-29 15:59:58.719    GME  2025-10-31  32.000  CALL       14           47  0.03            50        1           31   0.04            50
# 4  2025-10-29 15:59:59.533    GME  2025-10-31  21.500   PUT        1            7  0.03            50       53           11   0.05            50
# ..                     ...    ...         ...     ...   ...      ...          ...   ...           ...      ...          ...    ...           ...
# 73 2025-10-29 09:30:17.516    GME  2025-10-31  15.000   PUT        0            7  0.00            50       10            7   0.01            50
# 74 2025-10-29 15:59:59.318    GME  2025-10-31  31.000  CALL       14           69  0.03            50       21            9   0.04            50
# 75 2025-10-29 15:59:59.446    GME  2025-10-31  15.000  CALL      203           65  6.30            50      190           65  10.05            50
# 76 2025-10-29 15:57:02.263    GME  2025-10-31  20.500   PUT        0            5  0.00            50        1            5   0.03            50
# 77 2025-10-29 15:59:59.448    GME  2025-10-31  20.500  CALL      194           65  1.17            50      185           65   3.90            50



# df = option_snapshot_quote('GME', expiration='2025-10-31')

# df = option_snapshot_quote('GME', expiration='2025-11-07')

# df[df['right'] == 'CALL'].sort_values('strike', ascending=False).drop(columns=['bid_size', 'bid_exchange', 'bid_condition', 'ask_size', 'ask_exchange', 'ask_condition'])

# df[df['right'] == 'PUT'].sort_values('strike', ascending=False)


# df['strike'] = pd.to_numeric(df['strike'])


# df[(df['strike'] > 23) & (df['right'] == 'CALL')].sort_values('strike', ascending=False).drop(columns=['bid_size', 'bid_exchange', 'bid_condition', 'ask_size', 'ask_exchange', 'ask_condition'])



# df['expiration']


# df['bid'] * 100 / df['dte']

# df['premium_per_dte'] = df['bid'] * 100 / df['dte']
# # round to 2 decimal places
# df['premium_per_dte'] = df['premium_per_dte'].round(2)

# df['premium_per_dte'] / (df['strike'] * 100)

# df['premium_per_day_per_collateral'] = df['premium_per_dte'] / (df['strike'] * 100)

# df['ppdpc_pct'] = df['premium_per_day_per_collateral'] * 100
# df['ppdpc_pct'] = df['ppdpc_pct'].round(4)






# df = option_snapshot_quote('BMNR', expiration='2025-11-07')

# df = calculate_premium_metrics(df)

# df[(df['strike'] > 49.6) & (df['right'] == 'CALL')].sort_values('strike', ascending=False).drop(columns=['bid_size', 'bid_exchange', 'bid_condition', 'ask_size', 'ask_exchange', 'ask_condition'])


# # all expirations

# df = option_snapshot_quote('BMNR', expiration='*')
# df = calculate_premium_metrics(df)

# df.sort_values(by=['expiration', 'strike'], ascending=[True, False]).drop(columns=['bid_size', 'bid_exchange', 'bid_condition', 'ask_size', 'ask_exchange', 'ask_condition'])

# tmp = df[(df['strike'] > 49.6) & (df['right'] == 'CALL')].sort_values(by=['expiration', 'strike'], ascending=[True, False]).drop(columns=['bid_size', 'bid_exchange', 'bid_condition', 'ask_size', 'ask_exchange', 'ask_condition'])

# print(tmp.to_string())



# df['expiration'].sort_values().unique()

# # unique values of expiration sorted



# # for expiration in df['expiration'].unique():
# for expiration in df['expiration'].sort_values().unique():
#     # print(expiration)
#     tmp = df[(df['expiration'] == expiration) & (df['strike'] > 49.6) & (df['right'] == 'CALL')].sort_values(by=['strike'], ascending=[False]).drop(columns=['bid_size', 'bid_exchange', 'bid_condition', 'ask_size', 'ask_exchange', 'ask_condition'])
#     print(f"Expiration: {expiration}")
#     print(tmp.to_string())
#     print()




# # If I have a date `date`, calculate the number of days till then from today.
# from datetime import datetime, timedelta

# date = datetime(2025, 10, 31)
# today = datetime.now()

# days_until = (date - today).days

# # My date is in the format 'YYYY-MM-DD'
# date_str = '2025-10-31'
# date = datetime.strptime(date_str, '%Y-%m-%d')
# today = datetime.now()
# days_until = (date - today).days

# df['expiration']

# df


# df['expiration_date'] = pd.to_datetime(df['expiration'], format='%Y-%m-%d')
# today = pd.Timestamp.now().normalize()  # Get today's date at midnight
# df['dte'] = (df['expiration_date'] - today).dt.days

# # Drop the temporary expiration_date column
# df = df.drop('expiration_date', axis=1)



# import yfinance as yf
# from option_list_symbols import *

# symbols = option_list_symbols()

# df_all = pd.DataFrame()

# for item in symbols.head():
#     print(item)

# # iterate over symbols  


# for symbol in symbols['symbol']:
#     print(symbol)




# https://www.kaggle.com/datasets/andrewmvd/sp-500-stocks?resource=download

# open csv file in pandas
# df_sp500 = pd.read_csv('sp500_companies.csv')



# symbols = df_sp500['Symbol']



# # symbol = 'AAPL'
# # symbol = 'GME'

# import time

# count = 0

# start_time = time.time()

# # for symbol in symbols['symbol']:
# for symbol in symbols:
    
#     try:
#         print(f"Processing symbol: {symbol}")
#         df = option_snapshot_quote(symbol, expiration='*')
#         df = calculate_premium_metrics(df)

#         print(f"Getting underlying price for {symbol}...")
#         ticker = yf.Ticker(symbol)
#         current_price = ticker.history(period='1d')['Close'].iloc[-1]
#         df['underlying_price'] = current_price
#         # round to 2 decimal places
#         df['underlying_price'] = df['underlying_price'].round(2)

#         df_all = pd.concat([df_all, df], ignore_index=True)
#         # print(f"Symbol: {symbol}")
#         # print(df.sort_values(by=['expiration', 'strike'], ascending=[True, False]).drop(columns=['bid_size', 'bid_exchange', 'bid_condition', 'ask_size', 'ask_exchange', 'ask_condition']).to_string())
#         # print()
#     except Exception as e:
#         print(f"Error processing symbol {symbol}: {e}")
#         continue

#     count += 1
#     elapsed_time = time.time() - start_time
#     time_per_item = elapsed_time / (count)

#     estimated_total_time = time_per_item * len(symbols)

#     estimated_time_remaining = estimated_total_time - elapsed_time

#     # print(f"Processed {count} out of {len(symbols['symbol'])} symbols.")

#     # print(f"{count} / {len(symbols)} symbols processed. Elapsed time: {elapsed_time:.2f} seconds. Estimated time remaining: {estimated_time_remaining:.2f} seconds.")

#     print(f"{count} / {len(symbols)} symbols processed. Elapsed time: {elapsed_time:.2f} seconds. Estimated time remaining: {estimated_time_remaining / 60:.2f} minutes.")


# df_all['symbol'].nunique()  # number of unique symbols in




# # get current price for 'AMZN' using yfinance
# ticker = yf.Ticker('AMZN')
# current_price = ticker.history(period='1d')['Close'].iloc[-1]


# df_all

# df['in_the_money'] = df['right'] == 'CALL' & (df['underlying_price'] > df['strike'])

# df[df['right'] == 'CALL' & (df['underlying_price'] > df['strike'])]

# df['out_of_the_money'] = 

# df[(df['right'] == 'CALL') & (df['underlying_price'] < df['strike'])]

# (df['right'] == 'CALL') & (df['underlying_price'] < df['strike'])


# df[df['right'] == 'CALL']

# df.loc[df['right'] == 'CALL', 'out_of_the_money'] = df['underlying_price'] < df['strike']
# df.loc[df['right'] == 'PUT',  'out_of_the_money'] = df['underlying_price'] > df['strike']


# df = df_all

# df_oom = df[df['out_of_the_money'] == True]

# df_oom

# df_oom.sort_values(by=['ppdpc_pct'], ascending=False).head(50)


# tmp = df_oom[df_oom['dte'] > 6]
# tmp = tmp[tmp['dte'] <= 70]

# tmp.sort_values(by=['ppdpc_pct'], ascending=False).head(50).drop(columns=['premium_per_day_per_collateral', 'bid_exchange'])

