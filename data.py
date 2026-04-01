import os
from dotenv import load_dotenv
from massive import RESTClient
import pandas as pd
import datetime

load_dotenv()

client = RESTClient(os.getenv("MASSIVE_API_KEY"))

# Define a function to get the last day's close price of the stock

def get_stock_price(ticker):

    stock_lastinfo = client.get_previous_close_agg(
    ticker,
    adjusted="true",
    )
    return stock_lastinfo[0].close

# Define a function to obtain stock data from Massive

def get_options_data(ticker):
    options_chain = []
    for i, o in enumerate(client.list_snapshot_options_chain(
        ticker,
        params={
            "order": "asc",
            "sort": "ticker",
        },
    )): 
        options_chain.append(o)

    options_chain=pd.DataFrame(options_chain)

    details_df = pd.json_normalize(options_chain['details'])

    details_df=details_df[["contract_type", "expiration_date", "strike_price"]]

    greeks_df = pd.json_normalize(options_chain['greeks'])

    day_df = pd.json_normalize(options_chain['day'])

    options_chain=pd.concat([options_chain[["implied_volatility"]], day_df["close"], details_df, greeks_df], axis=1)


    options_chain["call"] = options_chain["contract_type"].map(lambda x: True if x.lower() == "call" else False)
    options_chain = options_chain.drop(columns=["contract_type"])

    options_chain["expiration_date"] = pd.to_datetime(options_chain["expiration_date"], utc=True)
    options_chain["DTE"] = (options_chain["expiration_date"] - datetime.datetime.now(datetime.timezone.utc)).dt.days + 1

     # Remove rows with DTE=0 to avoid division by zero in d_1
    options_chain =options_chain[options_chain["DTE"]!=0]
    options_chain = options_chain.dropna(subset=["close"])

    return options_chain