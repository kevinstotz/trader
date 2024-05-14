from dataclasses import dataclass
from enum import Enum
from typing import Any
from src.database.mydb import session
from src.models.trading_providers.coinbase import CoinbaseTradingModel, COINBASE_DATA_TABLE_NAME
from src.models.trading_providers.trading_provider import TradingProvider
from src.trading_providers.providers.coinbase_trading import CoinbaseTrading


@dataclass
class TradingProviderListDataMixin:
    table: str
    id: int
    row: int


class TradingProviderList(TradingProviderListDataMixin, Enum):
    COINBASE = COINBASE_DATA_TABLE_NAME, 1, 1


class TradingProviderFactory:
    provider_model: Any = None
    provider: Any = None
    client: Any = None

    def get_data_provider(self, provider_id=TradingProviderList.COINBASE.id) -> None:

        if provider_id == 0:
            self.provider = session.query(TradingProvider).filter(TradingProvider.is_active == 1).order_by(
                TradingProvider.priority).first()
        else:
            self.provider = session.query(TradingProvider).get(provider_id)

        if self.provider.id == TradingProviderList.COINBASE.id:
            self.provider_model: CoinbaseTradingModel = session.query(CoinbaseTradingModel).get(TradingProviderList.COINBASE.id)
            self.provider = CoinbaseTrading(self.provider_model.api_key, self.provider_model.api_secret)
            self.client = self.provider.get_client()
        else:
            print("cant get data provider")
            exit()

        session.close()
