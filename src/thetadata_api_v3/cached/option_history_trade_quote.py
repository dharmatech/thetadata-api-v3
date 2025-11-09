import pandas as pd
from thetadata_api_v3 import option_history_trade_quote as api_module
from thetadata_api_v3.cached.caching import CACHE_DIR
from datetime import datetime, time
from zoneinfo import ZoneInfo

def option_history_trade_quote(date: str, symbol: str, expiration: str, other_params: dict = None) -> pd.DataFrame:
    """
    Wrapper for option_history_trade_quote that uses a .pkl cache.
    """
    if other_params is None:
        other_params = {}

    diagnostics = False

    # Create a stable filename from other_params
    params_str = "-".join([f"{k}_{v}" for k, v in sorted(other_params.items())])
    filename = f"trade_quote-{date}-{symbol}-{expiration}-{params_str}.pkl"
    cache_path = CACHE_DIR / filename
    
    # Determine if we should bypass cache for today during market hours
    try:
        market_close_time = time(16, 0)
        eastern_tz = ZoneInfo("America/New_York")
        now_et = datetime.now(eastern_tz)
        request_date = datetime.strptime(date, '%Y-%m-%d').date()
        is_today_during_market_hours = (request_date == now_et.date() and now_et.time() < market_close_time)
    except Exception:
        is_today_during_market_hours = False # Fallback to not bypassing cache

    # If not today during market hours, try to read from cache
    if not is_today_during_market_hours and cache_path.exists():
        if diagnostics:
            print(f"CACHE HIT: Loading Trade/Quotes from {cache_path}")
        else:
            print('CH', end=' ', flush=True)
        return pd.read_pickle(cache_path)
        
    if diagnostics:
        if is_today_during_market_hours:
            print(f"CACHE BYPASS: Market is still open for {date}. Fetching from API.")
        else:
            print(f"CACHE MISS: Fetching Trade/Quotes from API for {date}")
    else:
        if not is_today_during_market_hours:
            print('CM', end=' ', flush=True)
        else:
            print('Market hours. Skipping cache.', end=' ', flush=True)

    df = api_module.option_history_trade_quote(date, symbol, expiration, other_params=other_params)
    
    # If we got data, and it's not today during market hours, save to cache
    if not df.empty and not is_today_during_market_hours:
        df.to_pickle(cache_path)
        
    return df