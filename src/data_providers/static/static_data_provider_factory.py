from dataclasses import dataclass
from enum import Enum
from typing import Any

from src.data_providers.providers.coinbase_data import CoinbaseData
from src.data_providers.static.alpaca_data import AlpacaData
from src.data_providers.static.coinbase_static import CoinbaseStaticData
from src.data_providers.static.polygon_io import PolygonIoData
from src.data_providers.static.yahoo_finance import YahooFinanceData
from src.data_providers.static.yfinance_module import YFinanceModule
from src.models.data_providers.coinbase import COINBASE_DATA_TABLE_NAME, CoinbaseDataModel
from src.models.static_data_providers.alpaca import ALPACA_TABLE_NAME, AlpacaModel
from src.models.static_data_providers.polygon_io import POLYGON_TABLE_NAME, PolygonIoModel
from src.models.static_data_providers.static_data_provider import StaticDataProvider
from src.database.mydb import session
from src.models.static_data_providers.yahoo_finance import YAHOO_FINANCE_TABLE_NAME, YahooFinanceModel


@dataclass
class StaticDataProviderListDataMixin:
    table: str
    id: int
    row: int


class StaticDataProviderList(StaticDataProviderListDataMixin, Enum):
    YAHOO_FINANCE = YAHOO_FINANCE_TABLE_NAME, 1, 1
    YFINANCE_MODULE = "YFINANCE_TABLE_NAME", 2, 1
    POLYGON_IO = POLYGON_TABLE_NAME, 3, 1
    ALPACA = ALPACA_TABLE_NAME, 4, 1
    COINBASE = COINBASE_DATA_TABLE_NAME, 5, 1


class StaticDataProviderFactory:
    provider_model: Any = None
    provider: Any = None
    client: Any = None

    def get_static_data_provider(self, provider_id=StaticDataProviderList.YAHOO_FINANCE.id) -> None:

        if provider_id == 0:
            self.provider = session.query(StaticDataProvider).filter(StaticDataProvider.is_active == 1).order_by(
                StaticDataProvider.priority).first()
        else:
            self.provider = session.query(StaticDataProvider).get(provider_id)
        if self.provider.id == StaticDataProviderList.YAHOO_FINANCE.id:
            print("YAHOO_FINANCE")
            self.provider_model: YahooFinanceModel = session.query(YahooFinanceModel).get(StaticDataProviderList.YAHOO_FINANCE.id)
            self.client: YahooFinanceData = YahooFinanceData(url=self.provider_model.endpoint)
        elif self.provider.id == StaticDataProviderList.YFINANCE_MODULE.id:
            print("YFINANCE_MODULE")
            self.client: YFinanceModule = YFinanceModule()
        elif self.provider.id == StaticDataProviderList.POLYGON_IO.id:
            print("POLYGON_IO")
            self.provider_model: PolygonIoModel = session.query(PolygonIoModel).get(StaticDataProviderList.POLYGON_IO.row)
            self.client: PolygonIoData = PolygonIoData(url=self.provider_model.endpoint, apikey=self.provider_model.api_key)
        elif self.provider.id == StaticDataProviderList.ALPACA.id:
            print("ALPACA")
            self.provider_model: AlpacaModel = session.query(AlpacaModel).get(StaticDataProviderList.ALPACA.row)
            self.client: AlpacaData = AlpacaData(api_key=self.provider_model.api_key, api_secret=self.provider_model.api_secret)
        elif self.provider.id == StaticDataProviderList.COINBASE.id:
            print("COINBASE")
            self.provider_model: CoinbaseDataModel = session.query(CoinbaseDataModel).get(StaticDataProviderList.COINBASE.row)
            self.client: CoinbaseStaticData = CoinbaseStaticData(api_key=self.provider_model.api_key,
                                                                 base_url=self.provider_model.base_url,
                                                                 api_secret=self.provider_model.api_secret)
        else:
            print("cant get data provider")
            exit()

        session.close()
