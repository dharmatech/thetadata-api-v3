
import httpx  # install via pip install httpx
import csv
import io
import pandas as pd

# https://docs.thetadata.us/operations/option_list_expirations.html

def option_list_expirations(symbol: str, format = None) -> pd.DataFrame:
    """
    Fetch option expiration dates for a given symbol.
    """
    BASE_URL = "http://localhost:25503/v3"  # all endpoints use this URL base

    params = {
        'symbol': symbol
    }
    
    if format is not None:
        params['format'] = format

    url = BASE_URL + '/option/list/expirations'

    results = []

    with httpx.stream("GET", url, params=params, timeout=60) as response:
        response.raise_for_status()  # make sure the request worked
        for line in response.iter_lines():
            for row in csv.reader(io.StringIO(line)):
                results.append(row)

    df = pd.DataFrame(results[1:], columns=results[0])

    return df

