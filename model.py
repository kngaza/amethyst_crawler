import contextlib
import multiprocessing

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, BigInteger, Date, Float, String

from connect import get_azure_engine

engine = get_azure_engine()
Base = automap_base()
Base.prepare(engine, reflect=True)


def init_model_daily():
    return Base.classes.Daily

def init_model_stockByDeal():
    return Base.classes.StockByDeal

@contextlib.contextmanager
def loadSession():
    """
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        # engine.dispose()

# a = {"ticker": "FLC", "trading_date":'22/03/2021',"price_close": 8.58,
#     "price_open": 8.3,"price_high":8.58,"price_low":8.2,"vol":45886600}