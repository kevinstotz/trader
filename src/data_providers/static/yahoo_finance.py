import datetime
from enum import Enum
from typing import Any
import urllib.parse
import pandas as pd
from environs import Env

from src.data_providers.static.static_abstract_data_provider import StaticDataProviderABC

env = Env()
env.read_env()


class Interval(Enum):
    DAY = "1d"
    WEEK = "1wk"
    MONTH = "1mn"


class YahooFinanceData(StaticDataProviderABC):

    def __init__(self, url="Url"):
        self.data = None
        self.url: str = url
        self.events: str = "history"
        self.includeAdjustedClose: str = "true"

    def get_client(self) -> Any:
        return self

    def get_data(self, ticker="NDAQ",
                 datetime_start=datetime.datetime(2022, 1, 1, 7, 35, 51),
                 datetime_end=datetime.datetime.today(),
                 interval=Interval.DAY.value) -> pd.DataFrame:

        timestamp_start = int(datetime_start.timestamp())
        timestamp_end = int(datetime_end.timestamp())
        params = {
            'period1': timestamp_start,
            'period2': timestamp_end,
            'interval': interval,
            'events': self.events,
            'includeAdjustedClose': self.includeAdjustedClose
        }
        url_string = urllib.parse.urljoin(self.url, ticker)
        url_string += "?" + urllib.parse.urlencode(params)
        self.data = pd.read_csv(url_string)
        return self.data

    def get_price(self):
        pass
