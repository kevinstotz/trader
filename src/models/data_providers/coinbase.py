from sqlalchemy import Boolean, insert, event, Integer, Float
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from environs import Env

from src.database.mydb import session, Base

env = Env()
env.read_env()

COINBASE_DATA_TABLE_NAME = "coinbase_data"
COINBASE_API_KEY = env.str("COINBASE_API_KEY", "nada")
COINBASE_API_SECRET = env.str("COINBASE_API_SECRET", "nada")
COINBASE_WSS_ENDPOINT = env.str("COINBASE_WSS_ENDPOINT", "nada")
COINBASE_BASE_URL = env.str("COINBASE_BASE_URL", "nada")


class CoinbaseDataModel(Base):
    __tablename__ = COINBASE_DATA_TABLE_NAME

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    api_key: Mapped[str] = mapped_column(String(255), default=COINBASE_API_KEY)
    api_secret: Mapped[str] = mapped_column(String(255), default=COINBASE_API_SECRET)
    wss_endpoint: Mapped[str] = mapped_column(String(255), default=COINBASE_WSS_ENDPOINT)
    active: Mapped[bool] = mapped_column(Boolean(), unique=False, default=True)
    base_url: Mapped[str] = mapped_column(String(255), default=COINBASE_BASE_URL)

    def __repr__(self) -> str:
        return f"CoinbaseDataModel(id={self.id!r}, key={self.api_key!r})"


@event.listens_for(CoinbaseDataModel.__table__, 'after_create')
def create_record(*args, **kwargs):
    session.execute(insert(CoinbaseDataModel).values())
    session.commit()
    session.close()
