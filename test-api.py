
from thetadata_api_v3.cached.option_history_greeks_all    import option_history_greeks_all
from thetadata_api_v3.cached.option_history_open_interest import option_history_open_interest

df = option_history_greeks_all(date='2025-10-27', symbol='GME', expiration='2025-10-31', interval='1h')

df = option_history_greeks_all(date='2025-10-27', symbol='GME', expiration='2025-10-31')

df_oi = option_history_open_interest(date='2025-10-27', symbol='GME', expiration='2025-10-31')

from thetadata_api_v3.cached.option_history_trade_quote import option_history_trade_quote

df_trade = option_history_trade_quote(date='2025-10-27', symbol='GME', expiration='2025-10-31')

df_trade
