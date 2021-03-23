import os
import json
import logging
import time

import schedule
import requests
from typing import List

from model import loadSession, init_model_stockByDeal

logging.basicConfig(filename='bydeallogging.log', level=os.environ.get("LOGLEVEL", "INFO"))

# API lấy dữ liệu theo từng lệnh khớp
URL_STOCK_TRADE: "https://bgapidatafeed.vps.com.vn/getliststocktrade/"
StockByDeal = init_model_stockByDeal()

def get_stock_by_deal(stocks: List):
    """Lấy dữ liệu theo từng lệnh khớp.
    Dữ liệu được lấy về theo dạng stack nên cần so sánh giá trị sID nếu mới hơn thì tiến hành insert.
    Định kỳ chạy 30s/lần
    """
    def get_latest_sid(stock):
        with loadSession() as session:
            rs = session.query(StockByDeal.sid).filter(StockByDeal.sym == stock).order_by(StockByDeal.trading_date).limit(1).all()
        return rs if rs else 0
    for stock in stocks:
        r = requests.get(URL_STOCK_TRADE + stock)
        raw = eval(r.text)
        latest_sid = get_latest_sid(stock)
        updated_data = next(row for row in raw if int(row["sID"] > latest_sid))
        updated_index = raw.index(updated_data)
        if updated_index:
            with loadSession() as session:
                session.execute(StockByDeal.insert(), raw[updated_data])
                session.commit()
            logging.info(f"Update for {stock}")
        else:
            continue

if __name__ == "__main__":
    with open("stock.json", "r") as f:
        stocks = json.load(f)
    schedule.every(30).seconds.do(get_stock_by_deal, stocks=stocks)
    while True:
        schedule.run_pending()
        time.sleep(1)