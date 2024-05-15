from abc import ABC, abstractmethod
from typing import Any


class TradingProviderABC(ABC):

    @abstractmethod
    def get_client(self,) -> Any:
        ...

    @abstractmethod
    def create_order(self, order_id: str, product: str, size: int) -> dict:
        ...

    @abstractmethod
    def get_order(self, order_id: str) -> dict:
        ...

    @abstractmethod
    def cancel_order(self, order_id: str) -> dict:
        ...
