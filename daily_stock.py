import os
import time
import json
from datetime import date, datetime, timedelta
import logging

import schedule
import requests
from typing import List

from utils import logger

logging.basicConfig(filename='dailylogging.log', level=os.environ.get("LOGLEVEL", "INFO"))
# API lấy dữ liệu cuối ngày
URL_STOCK_EOD: "https://histdatafeed.vps.com.vn/tradingview/history?symbol={}&resolution=1D&from={}&to={}"

def get_daily_stock(stocks: List, _from: int = None) -> None:
    """Lấy dữ liệu cuối ngày và cập nhật vào CSDL.
    Nếu dữ liệu tại thời điểm call bằng với mã đã trong lịch sử thì bỏ qua.
    Nếu dữ liệu tại thời điểm call khác với mã đã có trong lịch sử thì tiến hành call lại toàn bộ
    và update lại dữ liệu mã đó.
    Định kỳ: mỗi ngày 1 lần vào lúc 23:00PM
    Params:
    ----
     - stocks (List): danh sách mã 
     - _from (int{unix timestamp}): lấy dữ liệu từ ngày nào, mặc định sẽ lấy từ ngày trước thời điểm gọi api

    Returns:
    ----
    """
    _to = int(time.time())
    if not _from:
        yesterday = (datetime.today() - timedelta(1)).timestamp()
        _from = int(yesterday)

    for stock in stocks:
        r = requests.get(URL_STOCK_EOD.format(stock, _from, _to))
        raw = eval(r.text)
        if raw["s"] == "ok":
            # Check giá trị -> update

            # insert
            pass
        else:
            date_to_str = date.fromtimestamp(_to).strftime("%Y/%m/%d")
            logging.warning(f"Dữ liệu cuối ngày {date_to_str} của {stock} không tồn tại")
            continue


def init_daily_stock(stocks):
    """Khởi tạo dữ liệu cho toàn bộ mã
    """
    get_daily_stock(stocks, _from=967334400)
    return schedule.CancelJob


if __name__ == "__main__":
    with open("stock.json", "r") as f:
        stocks = json.load(f)
    schedule.every().day.at("23:00").do(init_daily_stock, stocks=stocks)
    schedule.every().day.at("23:00").do(get_daily_stock, stocks=stocks)
    while True:
        schedule.run_pending()
        time.sleep(1)
