from datetime import datetime 

import pandas as pd
from typing import Dict
import requests


def transformer_for_daily_stock(stock: str, raw: Dict):
    """
    """
    df = pd.DataFrame(raw)
    df.drop("s", axis=1, inplace=True)
    df.columns = ['trading_date', 'price_close', 'price_open', 'price_high', 'price_low', 'volumn']
    df.ticker = stock
    df["trading_date"] = df["trading_date"].apply(lambda x: datetime.fromtimestamp(x)\
        .strftime("%Y/%m/%d"))

    return df.to_dict('records')


def transformer_for_stock_by_deal(raw:Dict):
    """
    """
    df = pd.DataFrame(raw)
    df.drop(['id', 'cl', 'ch', 'lc', 'ca', 'timeServer', 'lv'], axis=1, inplace=True)
    return df.to_dict('records')