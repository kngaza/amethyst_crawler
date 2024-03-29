import os

import urllib
import pyodbc
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_azure_engine():
    """Tạo Azure engine để connect
    """
    params = urllib.parse.quote_plus \
        (f'Driver={os.getenv("DRIVER")};'
        f'Server=tcp:{os.getenv("SERVER")},1433;'
        f'Database={os.getenv("DATABASE")};'
        f'Uid={os.getenv("USERNAME")};'
        f'Pwd={os.getenv("PASSWORD")};'
        f'Encrypt=yes;'
        f'TrustServerCertificate=no;Connection Timeout=30;')
    conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    engine_azure = create_engine(conn_str)

    return engine_azure


if __name__ == "__main__":
    engine = get_azure_engine()
    print(engine.table_names())