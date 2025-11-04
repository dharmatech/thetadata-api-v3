import httpx  # install via pip install httpx
import csv
import io
import pandas as pd

# It seems like this is not cachable since it may still be active when we call it.
# For expirations in the past, those we can consider caching.

# https://docs.thetadata.us/operations/option_list_dates.html

def option_list_dates(request_type, symbol, expiration, other_params=None):
    BASE_URL = "http://localhost:25503/v3"

    params = {
        'symbol': symbol,
        'expiration': expiration,
    }

    if other_params:
        params.update(other_params)

    url = BASE_URL + f'/option/list/dates/{request_type}'

    results = []

    with httpx.stream("GET", url, params=params, timeout=60) as response:
        response.raise_for_status()  # make sure the request worked
        for line in response.iter_lines():
            for row in csv.reader(io.StringIO(line)):
                results.append(row)

    df = pd.DataFrame(results[1:], columns=results[0])

    return df

