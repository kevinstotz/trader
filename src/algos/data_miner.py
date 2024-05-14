import importlib
from types import ModuleType
import pandas as pd
from enum import Enum
from sqlalchemy import text
from src.database.mydb import session


class Units(Enum):
    DAY = "DAY"
    HOUR = "HOUR"
    MINUTE = "MINUTE"


class DataMiner:
    module: ModuleType = None
    data: pd.DataFrame
    hour: int = 23
    minute: int = 59

    def __init__(self, ticker="BTC-USD", units=Units.DAY, period=365, start_date="2024-01-01", start_time="00:00:00"):
        self.start_date: str = start_date
        self.start_time: str = start_time
        self.ticker: str = ticker
        self.units: Units = units
        self.period: int = period

    def get_data(self) -> pd.DataFrame:
        try:
            self.module = importlib.import_module(
                'src.models.crypto_pairs.' + self.ticker.lower().replace('-', '_'))
        except:
            exit(1)
        minutes: str = ""
        hours: str = ""

        if self.units == Units.DAY:
            self.hour = 23
            self.minute = 59
            hours = "HOUR(timestamp) = " + str(self.hour) + " and "
            minutes = "MINUTE(timestamp) = " + str(self.minute) + " and "
        if self.units == Units.HOUR:
            self.minute = 0
            minutes = "MINUTE(timestamp) = " + str(self.minute) + " and "
            hours = ""
        if self.units == Units.MINUTE:
            self.hour = 0
            self.minute = 0
            minutes = ""
            hours = ""

        data = {
            "table": "crypto_data." + self.ticker.lower().replace('-', '_'),
            "minute": self.minute,
            "hour": self.hour,
            "period": self.period,
            "units": self.units.value,
        }
        sql = "".join(["SELECT timestamp, high+0.0, low+0.0, open+0.0, close+0.0 ",
                       "FROM ",
                       data['table'],
                       " WHERE ",
                       minutes,
                       hours,
                       "STR_TO_DATE(timestamp, '%Y-%m-%d %T') > CURDATE() - INTERVAL ",
                       str(self.period),
                       " ",
                       data['units']])

        statement = text(sql)
        res = session.execute(statement)
        self.data = pd.DataFrame.from_records(data=res,
                                              index='timestamp',
                                              columns=['timestamp', 'high', 'low', 'open', 'close'])
        print(self.data.describe())
        self.data.index = pd.to_datetime(self.data.index)
        print(self.data.head(5))
        return self.data
