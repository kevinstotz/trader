import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass
class DataResponse:
    status: str
    text: str
    dt: float


class StaticDataProviderABC(ABC):

    @abstractmethod
    def get_client(self) -> Any:
        ...

    def get_data(self,
                 ticker: str,
                 start: datetime.datetime,
                 end: datetime.datetime,
                 interval: str = "1d"
                 ) -> pd.DataFrame:
        ...
