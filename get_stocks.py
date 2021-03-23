import json
import time

import requests
import schedule

# Danh sách sàn
LIST_STOCK_EXCHANGE: ['hose', 'vn30', 'upcom']
# API lấy danh sách stock
URL_GET_STOCK: "https://bgapidatafeed.vps.com.vn/getlistckindex/"

def get_stocks():
    """Lấy danh sách mã ck, vì mã này có thể thay đổi và là đầu vào cho 2 crawler
    nên dữ liệu sau khi được lấy về sẽ lưu thành file.
    Định kỳ chạy: mỗi ngày 1 lần vào lúc 7:00AM
    """
    stock = []
    for name in LIST_STOCK_EXCHANGE:
        r = requests.get(URL_GET_STOCK + name)
        stock.extend(eval(r.content))
        time.sleep(5)

    with open("stock.json", "w") as f:
        json.dump(stock, f)


if __name__ == "__main__":
    schedule.every().day.at("07:00").do(get_stocks)
    while True:
        schedule.run_pending()
        time.sleep(1)