from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class DataResponse:
    status: str
    text: str
    dt: float


class DataProviderABC(ABC):

    @abstractmethod
    def get_client(self) -> Any:
        ...
