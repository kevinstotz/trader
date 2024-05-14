from enum import Enum
from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient, StockLatestQuoteRequest, \
    StockBarsRequest, CryptoBarsRequest, CryptoLatestQuoteRequest, TimeFrame
import datetime
from typing import Any
import pandas as pd

from src.data_providers.static.static_abstract_data_provider import StaticDataProviderABC


class Period(Enum):
    DAY = "1d"
    FIVE_DAY = "5d"
    MONTH = "1mo"
    THREE_MONTH = "3m"
    SIX_MONTH = "6m"
    YEAR = "1y"
    TWO_YEAR = "2y"
    FIVE_YEAR = "5y"
    HOUR = "1h"
    MINUTE = "1m"
    TWO_MINUTE = "2m"
    FIVE_MINUTE = "5m"
    FIFTEEN_MINUTE = "15m"
    THIRTY_MINUTE = "30m"
    SIXTY_MINUTE = "60m"
    NINTY_MINUTE = "90m"


class AlpacaData(StaticDataProviderABC):
    data = None
    ticker = None
    client = None

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_client(self) -> Any:
        return self.client

    def get_data(self, ticker="NDAQ",
                 datetime_start=datetime.datetime(2024, 5, 1, 7, 35, 51),
                 datetime_end=datetime.datetime.today(),
                 interval=Period.DAY.value) -> pd.DataFrame:
        self.client = StockHistoricalDataClient(self.api_key, self.api_secret)
        request = StockBarsRequest(symbol_or_symbols=[ticker],
                                   timeframe=TimeFrame.Day,
                                   start=datetime_start,
                                   end=datetime_end)
        bars = self.client.get_stock_bars(request)
        self.data = bars.df
        return self.data

    def get_crypto_data(self,
                        ticker="BTC/USD",
                        datetime_start=datetime.datetime(2024, 5, 1, 7, 35, 51),
                        datetime_end=datetime.datetime.today(),
                        interval=Period.DAY.value) -> pd.DataFrame:
        self.client = CryptoHistoricalDataClient()
        request = CryptoBarsRequest(symbol_or_symbols=[ticker],
                                    timeframe=TimeFrame.Day,
                                    start=datetime_start,
                                    end=datetime_end)
        bars = self.client.get_crypto_bars(request)
        self.data = bars.df
        return self.data

    def get_stock_price(self, ticker="NDAQ") -> dict:
        # multi symbol request - single symbol is similar
        multi_symbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=[ticker])
        self.data = self.client.get_stock_latest_quote(multi_symbol_request_params)
        print(self.data)
        return self.data

    def get_crypto_price(self, ticker="BTC/USD") -> dict:
        self.client = CryptoHistoricalDataClient()
        multi_symbol_request_params = CryptoLatestQuoteRequest(symbol_or_symbols=[ticker])
        self.data = self.client.get_crypto_latest_quote(multi_symbol_request_params)
        print(self.data)
        return self.data
