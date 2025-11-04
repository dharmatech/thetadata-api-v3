import httpx  # install via pip install httpx
import csv
import io
import pandas as pd



# https://docs.thetadata.us/operations/option_history_open_interest.html

def option_history_open_interest(date: str, symbol: str, expiration: str, other_params: dict = None) -> pd.DataFrame:
    """
    Fetches option open interest history for a given date, symbol, and expiration.
    """
    BASE_URL = "http://localhost:25503/v3"  # all endpoints use this URL base

    params = {
      'date': date,
      'symbol': symbol,
      'expiration': expiration,
    }

    if other_params:
        params.update(other_params)

    url = BASE_URL + '/option/history/open_interest'

    results = []

    with httpx.stream("GET", url, params=params, timeout=60) as response:
        response.raise_for_status()  # make sure the request worked
        for line in response.iter_lines():
            for row in csv.reader(io.StringIO(line)):
                results.append(row)

    df = pd.DataFrame(results[1:], columns=results[0])

    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')

    return df


# import importlib

# import thetadata_api_v3.option_history_open_interest

# importlib.reload(thetadata_api_v3.option_history_open_interest)

# from thetadata_api_v3.option_history_open_interest import option_history_open_interest

# df = option_history_open_interest('2025-10-30', 'GME', '2025-11-07')

# df = option_history_open_interest('2025-10-29', 'GME', '2025-11-07')

# df = option_history_open_interest('2025-10-28', 'GME', '2025-11-07')



# df = option_history_open_interest('2025-10-28', 'RKT', '2025-10-31')