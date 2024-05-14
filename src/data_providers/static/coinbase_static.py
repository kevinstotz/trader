import datetime
import json
from enum import Enum
from typing import Any
from json import dumps

import pandas as pd

from src.data_providers.static.static_abstract_data_provider import StaticDataProviderABC
from coinbase.rest import RESTClient


class Interval(Enum):
    MINUTE = "ONE_MINUTE"
    FIVE_MINUTE = "FIVE_MINUTE"
    FIFTEEN_MINUTE = "FIFTEEN_MINUTE"
    THIRTY_MINUTE = "THIRTY_MINUTE"
    ONE_HOUR = "ONE_HOUR"
    TWO_HOUR = "TWO_HOUR"
    SIX_HOUR = "SIX_HOUR"
    ONE_DAY = 'ONE_DAY'


class CoinbaseStaticData(StaticDataProviderABC):
    data: pd.DataFrame = None
    client: RESTClient
    api_key: str = ""
    api_secret: str = ""
    timeout: int = 5
    base_url: str
    product: dict = {}

    def __init__(self,
                 base_url: str,
                 api_key: str = "",
                 api_secret: str = "",
                 timeout: int = 5
                 ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout
        self.base_url = base_url
        self.client = RESTClient(api_key=self.api_key,
                                 api_secret=self.api_secret,
                                 timeout=self.timeout)

    def get_client(self) -> Any:
        return self.client

    def get_data(self,
                 ticker="BTC-USD",
                 datetime_start=datetime.datetime(2024, 5, 10, 0, 0, 0),
                 datetime_end=datetime.datetime.today(),
                 interval=Interval.ONE_HOUR.value
                 ) -> pd.DataFrame:

        result = self.client.get_candles(
            product_id=ticker,
            start=int(datetime_start.timestamp()),
            end=int(datetime_end.timestamp()),
            granularity=interval
        )

        self.data = pd.read_json(json.dumps(result['candles']))
        self.data = self.data.rename(columns={"start": "timestamp"})
        self.data = self.data.set_index("timestamp")

        return self.data

    def get_price(self, ticker="BTC-USD") -> dict:
        self.product = self.client.get_product(product_id=ticker)
        return self.product
