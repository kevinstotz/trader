from enum import Enum
import yfinance as yfin
import datetime
from typing import Any
import pandas as pd

from src.data_providers.static.static_abstract_data_provider import StaticDataProviderABC


class Period(Enum):
    DAY = "1d"
    FIVE_DAY = "5d"
    WEEK = "1wk"
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


class YFinanceModule(StaticDataProviderABC):
    data = None
    ticker = None

    def get_client(self) -> Any:
        return self

    def get_data(self, ticker="NDAQ",
                 datetime_start=datetime.datetime(2022, 1, 1, 7, 35, 51),
                 datetime_end=datetime.datetime.today(),
                 interval=Period.DAY.value) -> pd.DataFrame:
        self.ticker = yfin.Ticker(ticker)
        self.data = self.ticker.history(period=interval)

        return self.data
