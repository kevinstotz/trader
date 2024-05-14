from dataclasses import dataclass
from enum import Enum
from typing import Any
from src.models.data_providers.data_provider import DataProvider
from src.database.mydb import session
from src.models.data_providers.coinbase import CoinbaseDataModel, COINBASE_DATA_TABLE_NAME
from src.data_providers.providers.coinbase_data import CoinbaseData


@dataclass
class DataProviderListDataMixin:
    table: str
    id: int
    row: int


class DataProviderList(DataProviderListDataMixin, Enum):
    COINBASE = COINBASE_DATA_TABLE_NAME, 1, 1


class DataProviderFactory:
    provider_model: Any = None
    provider: Any = None
    client: Any = None

    def get_data_provider(self, provider_id=DataProviderList.COINBASE.id) -> None:

        if provider_id == 0:
            self.provider = session.query(DataProvider).filter(DataProvider.is_active == 1).order_by(
                DataProvider.priority).first()
        else:
            self.provider = session.query(DataProvider).get(provider_id)

        if self.provider.id == DataProviderList.COINBASE.id:
            self.provider_model: CoinbaseDataModel = session.query(CoinbaseDataModel).get(DataProviderList.COINBASE.id)
            self.provider = CoinbaseData(self.provider_model.api_key, self.provider_model.api_secret)
            self.client = self.provider.get_client()
        else:
            print("cant get data provider")
            exit()

        session.close()
