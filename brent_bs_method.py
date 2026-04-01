import numpy as np
from scipy.special import ndtr
from scipy.optimize import root_scalar
from config import lower_bound, upper_bound, risk_free_rate

# Black-Scholes formulas for call and put options

Phi=ndtr

def bs_call_price(vol, time_to_expiry, strike_price, stock_lastprice, risk_free_rate):
    d_1 =(np.log(stock_lastprice/strike_price) + (risk_free_rate + vol**2/2) * time_to_expiry)/ (vol * np.sqrt(time_to_expiry))

    d_2 = d_1 - vol * np.sqrt(time_to_expiry)

    term_1 = stock_lastprice * Phi(d_1)

    term_2 = strike_price * np.exp(-risk_free_rate * time_to_expiry) * Phi(d_2)

    return term_1-term_2

def bs_put_price(vol, time_to_expiry, strike_price, stock_lastprice, risk_free_rate):
    d_1 = (np.log(stock_lastprice/strike_price) + (risk_free_rate + vol**2/2) * time_to_expiry) /(vol * np.sqrt(time_to_expiry))

    d_2 = d_1 - vol * np.sqrt(time_to_expiry)

    term_1 = strike_price * np.exp(-risk_free_rate * time_to_expiry) * Phi(-d_2)

    term_2 = stock_lastprice * Phi(-d_1)

    return term_1-term_2

# Use Brent's method (root_scalar with brentq) to solve for implied volatility


def brent_bs_method(time_to_expiry, strike_price, stock_lastprice, risk_free_rate, option_marketprice, call):
    if call:
        def bs_model(x):
            return bs_call_price(x,time_to_expiry, strike_price, stock_lastprice, risk_free_rate) - option_marketprice
    else:
        def bs_model(x):
            return bs_put_price(x,time_to_expiry, strike_price, stock_lastprice, risk_free_rate) - option_marketprice
    try:
        res = root_scalar(bs_model, method="brentq", bracket=[lower_bound, upper_bound])
        return res.root if res.converged else None
    except:
        return None