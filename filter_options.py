import numpy as np
from config import lower_bound, upper_bound, risk_free_rate
from data import get_options_data, get_stock_price
from brent_bs_method import brent_bs_method

# We define a function to exclude data of which iv is not computable and the ITM options 

def get_vol_surface_data(ticker):

    options=get_options_data(ticker)
    strike_prices = options["strike_price"].to_numpy()
    DTEs = options["DTE"].to_numpy()
    massive_ivs = options["implied_volatility"].to_numpy()
    calls = options["call"].to_numpy()
    closes = options["close"].to_numpy()

    stock_last_price = get_stock_price(ticker)

    IVs = [brent_bs_method(days_to_expiry/365, strike_price, stock_last_price ,risk_free_rate, option_marketprice, is_call)
            for days_to_expiry, strike_price, option_marketprice, is_call in zip(DTEs, strike_prices, closes, calls)]


    options["computed_iv"]=IVs

    iv_filter = np.array([iv is not None for iv in IVs])


    # Filter out the ITM options 

    call_filter=(options["strike_price"] < stock_last_price + 10)& (options["call"])

    put_filter=(options["strike_price"] > stock_last_price - 10)& (~options["call"])

    final_filter=iv_filter & (call_filter | put_filter)


    return options[final_filter]