import os
import requests
from datetime import datetime
from financial.models.model import FinancialData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pymysql
pymysql.install_as_MySQLdb()
load_dotenv()

# load env
API_KEY = os.environ.get("API_KEY")
STOCK_API_URL = os.environ.get("STOCK_API_URL")
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class StockFinancialData:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None

    def fetch_financial_data(self):
        """
            function to fetch financial data from api
        """
        response = requests.get(STOCK_API_URL, params={
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": self.symbol,
            "apikey": API_KEY
        })

        if response.status_code == 200:
            self.data = response.json()
            return self.process_financial_data()
        else:
            print('There is no target stock: {} !'.format(self.symbol))
            return []

    def process_financial_data(self):
        """
            function to process financial data, get recent 14 days info
        """
        trade_series = self.data.get("Time Series (Daily)", {})
        result = []

        try:
            for trade_date, trade_info in trade_series.items():
                record_date = datetime.strptime(trade_date, "%Y-%m-%d")
                if (datetime.today() - record_date).days <= 14:
                    open_price = trade_info.get('1. open', '')
                    close_price = trade_info.get('4. close', '')
                    vol = trade_info.get('6. volume', '')
                    result.append(FinancialData(
                        symbol=self.symbol,
                        date=trade_date,
                        open_price=open_price,
                        close_price=close_price,
                        volume=vol))
            return result
        except Exception as e:
            print('Process current data failed! {}'.format(e))
            return []


def insert_into_db(trade_info_series):
    """
        function to insert processed data into db
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URI, )
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for trade_info in trade_info_series:
        # skip duplicated data in db
        if session.query(FinancialData).filter_by(symbol=trade_info.symbol, date=trade_info.date).first():
            continue
        session.add(trade_info)
    session.commit()
    session.close()


def main_func():
    stocks = ["IBM", "AAPL"]
    for stock in stocks:
        instance = StockFinancialData(stock)
        trade_data = instance.fetch_financial_data()
        if trade_data:
            insert_into_db(trade_data)

if __name__ == '__main__':
    main_func()

