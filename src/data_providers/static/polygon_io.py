import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Any
import urllib.request
import urllib.parse
import pandas as pd
from environs import Env
import json
from src.data_providers.static.static_abstract_data_provider import StaticDataProviderABC

env = Env()
env.read_env()


@dataclass
class PolyGonIoResponse:
    ticker: str
    queryCount: int
    resultsCount: int
    adjusted: bool
    results: []
    status: str
    request_id: str
    count: int


class Period(Enum):
    SECOND = "second",
    MINUTE = "minute",
    HOUR = "hour",
    DAY = "day",
    MONTH = "month",
    WEEK = "week",
    QUARTER = "quarter",
    YEAR = "year"


class PolygonIoData(StaticDataProviderABC):
    api_key = None

    def __init__(self, apikey, url="Url"):
        self.data = None
        self.url: str = url
        self.api_key = apikey

    def get_client(self) -> Any:
        return self

    def get_data(self,
                 ticker="NDAQ",
                 datetime_start=datetime.datetime(2024, 5, 1, 0, 0, 0),
                 datetime_end=datetime.datetime.today(),
                 interval=1,
                 period=Period.DAY.value) -> pd.DataFrame:
        url_string = urllib.parse.urljoin(self.url, ticker)
        url_string += "/"
        url_string += "range"
        url_string += "/"
        url_string += str(interval)
        url_string += "/"
        url_string += period[0]
        url_string += "/"
        url_string += datetime_start.strftime("%Y-%m-%d")
        url_string += "/"
        url_string += datetime_end.strftime("%Y-%m-%d")
        url_string += "?"
        url_string += "apiKey="
        url_string += self.api_key
        contents = urllib.request.urlopen(url_string).read()
        result = json.loads(contents)
        self.data = pd.read_json(json.dumps(result["results"]))
        self.data = self.data.rename(columns={
            "v": "volume",
            "vw": "vwa",
            "o": "open",
            "c": "close",
            "h": "high",
            "l": "low",
            "t": "timestamp",
            "n": "transactions"
        })

        return self.data
