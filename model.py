import contextlib
import multiprocessing

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, Date, Float, String

from connect import get_azure_engine

engine = get_azure_engine()
Base = declarative_base(engine)
# Base.prepare(engine, reflect=True)

class Daily(Base):
    """ORM cho bảng Daily
    """
    __tablename__ = "Daily"
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    trading_date = Column(Date)
    price_close = Column(Float)
    price_open = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    volumn = Column(BigInteger)


class StockByDeal(Base):
    """ORM cho bảng StockByDeal
    """
    __tablename__ = "StockByDeal"
    sid = Column(BigInteger, primary_key=True)
    sym = Column(String)
    trading_date = Column(Date)
    lastPrice = Column(Float)
    lastVol = Column(Integer)
    change = Column(Float)
    changePc = Column(Float)
    totalVol = Column(Integer)
    hp = Column(Float)
    lp = Column(Float)
    ap = Column(Float)


@contextlib.contextmanager
def loadSession():
    """
    """
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()

a = {"ticker": "FLC", "trading_date":'22/03/2021',"price_close": 8.58,"price_open": 8.3,"price_high":8.58,"price_low":8.2,"vol":45886600}
if __name__ == "__main__":
    daily = Daily()
    with loadSession() as session:
        session.execute(daily.insert(), a)
