import pandas as pd
from thetadata_api_v3 import option_history_open_interest as api_module
from thetadata_api_v3.cached.caching import CACHE_DIR

def option_history_open_interest(date, symbol, expiration):
    """
    Wrapper for option_history_open_interest that uses a .pkl cache.
    """

    diagnostics = True

    filename = f"oi-{symbol}-{expiration}-{date}.pkl"
    cache_path = CACHE_DIR / filename
    
    if cache_path.exists():
        if diagnostics:
            print(f"CACHE HIT: Loading OI from {cache_path}")
        else:
            print('CH', end=' ', flush=True)
        return pd.read_pickle(cache_path)

    if diagnostics:    
        print(f"CACHE MISS: Fetching OI from API for {date}")
    else:
        print('CM', end=' ', flush=True)

    # print(f'in get_cached_oi: {date} {symbol} {expiration}')

    df = api_module.option_history_open_interest(date, symbol, expiration)
    if not df.empty:
        df.to_pickle(cache_path)
    return df

