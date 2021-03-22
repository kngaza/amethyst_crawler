import os
import json
import logging

import requests
import hydra
from typing import List

from model import loadSession, Daily, StockByDeal


@hydra.main(config_name="config.yaml")
def get_stock_by_deal(stocks: List, cfg):
    """
    """
    def get_latest_sid(stock):
        with loadSession() as session:
            rs = session.query(StockByDeal.sid).filter(StockByDeal.sym == stock).order_by(StockByDeal.trading_date).limit(1)
        return rs if rs else 0
    for stock in stocks:
        r = requests.get(cfg.URL_STOCK_TRADE + stock)
        raw = eval(r.text)
        latest_sid = get_latest_sid(stock)
        updated_data = next(row for row in raw if int(row["sID"] > latest_sid))
        updated_index = raw.index(updated_data)
        if updated_index:
            with loadSession() as session:
                session.execute(Daily.insert(), raw[updated_data])
                session.commit()
        else:
            continue

if __name__ == "__main__":
    with open("stock.json", "r") as f:
        stocks = json.load(f)
    get_stock_by_deal(stocks)