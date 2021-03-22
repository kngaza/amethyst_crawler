import os
import time
import json
from datetime import date, datetime, timedelta
import logging

import hydra
import requests
from typing import List

from utils import logger

logging.basicConfig(filename='dailylogging.log', level=os.environ.get("LOGLEVEL", "INFO"))

@hydra.main(config_name="config.yaml")
def get_stock_eod(stocks: List, cfg, _from: int = None, _to: int = None):
    """
    """
    _to = int(time.time())
    if not _from:
        _from = 967334400
    else:
        yesterday = (datetime.today() - timedelta(1)).timestamp()
        _from = int(yesterday)
    for stock in stocks:
        r = requests.get(cfg.URL_STOCK_EOD.format(stock, _from, _from, _to))
        raw = eval(r.text)
        if raw["s"] == "ok":
            pass
        else:
            date_to_str = date.fromtimestamp(_to).strftime("%Y/%m/%d")
            logging.warning(f"Dữ liệu cuối ngày {date_to_str} của {stock} không tồn tại")
            continue


if __name__ == "__main__":
    with open("stock.json", "r") as f:
        stocks = json.load(f)
    get_stock_eod(stocks)