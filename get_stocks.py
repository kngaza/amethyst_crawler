import json
import time

import requests
import hydra


@hydra.main(config_name="config.yaml")
def get_stocks(cfg):
    """
    """
    stock = []
    for name in cfg.LIST_STOCK_EXCHANGE:
        r = requests.get(cfg.URL_GET_STOCK + name)
        stock.extend(eval(r.content))
        time.sleep(5)

    with open("stock.json", "w") as f:
        json.dump(stock, f)


if __name__ == "__main__":
    get_stocks()