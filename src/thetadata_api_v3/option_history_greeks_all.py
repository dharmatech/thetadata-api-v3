import httpx  # install via pip install httpx
import csv
import io
import pandas as pd

def option_history_greeks_all(date, symbol, expiration, interval=None):
    BASE_URL = "http://localhost:25503/v3"  # all endpoints use this URL base

    params = {
      'date': date,
      'symbol': symbol,
      'expiration': expiration,
      # 'interval': interval,
    }

    if interval is not None:
        params['interval'] = interval
   
    url = BASE_URL + '/option/history/greeks/all'

    results = []

    with httpx.stream("GET", url, params=params, timeout=60) as response:
        response.raise_for_status()  # make sure the request worked
        for line in response.iter_lines():
            for row in csv.reader(io.StringIO(line)):
                results.append(row)

    
    df = pd.DataFrame(results[1:], columns=results[0])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# from thetadata_api_v3.option_history_greeks_all import option_history_greeks_all

# df = option_history_greeks_all('2025-10-29', 'GME', '2025-10-31', interval='1h')
# df = option_history_greeks_all('2025-10-30', 'GME', '2025-10-31', interval='1h')

# https://discord.com/channels/937472081443037214/947695521466834984/1433440115828723813
# 
# Data for previous day is unavailable during midnight - 01:45 am ET
#
# 00:00 to 01:45 ET
# 21:00 to 22:45 PT


# df

# df.iloc[0]

# BASE_URL = "http://localhost:25503/v3"  # all endpoints use this URL base

# # set params
# params = {
#   'date': '2024-11-07',
#   'symbol': 'AAPL',
#   'expiration': '2025-01-17',
#   'interval': '1m',
# }

# #
# # This is the streaming version, and will read line-by-line
# #
# url = BASE_URL + '/option/history/greeks/all'

# results = []

# with httpx.stream("GET", url, params=params, timeout=60) as response:
#     response.raise_for_status()  # make sure the request worked
#     for line in response.iter_lines():
#         for row in csv.reader(io.StringIO(line)):
#             results.append(row)

# import pandas as pd
# df = pd.DataFrame(results[1:], columns=results[0])
# df['timestamp'] = pd.to_datetime(df['timestamp'])
# print(df)

# tbl = df.drop(columns=['d1', 'd2', 'speed', 'zomma', 'color', 'charm', 'veta', 'ultima', 'vomma', 'vera'])

# tbl.sort_values(by=['gamma'])
# tbl.sort_values(by=['vanna'])

