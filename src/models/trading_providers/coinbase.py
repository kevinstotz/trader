from sqlalchemy import Boolean, insert, event, Integer, Float
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from environs import Env

from src.database.mydb import session, Base

env = Env()
env.read_env()

COINBASE_TRADING_TABLE_NAME = "coinbase_trading"
COINBASE_API_KEY = env.str("COINBASE_API_KEY", "nada")
COINBASE_API_SECRET = env.str("COINBASE_API_SECRET", "nada")
COINBASE_TESTING_API_KEY = env.str("COINBASE_TESTING_API_KEY", "nada")
COINBASE_TESTING_API_SECRET = env.str("COINBASE_TESTING_API_SECRET", "nada")


class CoinbaseTradingModel(Base):
    __tablename__ = COINBASE_TRADING_TABLE_NAME

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    api_key: Mapped[str] = mapped_column(String(255), default=COINBASE_API_KEY)
    api_secret: Mapped[str] = mapped_column(String(255), default=COINBASE_API_SECRET)
    testing_api_key: Mapped[str] = mapped_column(String(255), default=COINBASE_TESTING_API_KEY)
    testing_api_secret: Mapped[str] = mapped_column(String(255), default=COINBASE_TESTING_API_SECRET)
    maker_fee: Mapped[float] = mapped_column(Float, default=0.0)
    taker_fee: Mapped[float] = mapped_column(Float, default=0.0)
    active: Mapped[bool] = mapped_column(Boolean(), unique=False, default=True)

    def __repr__(self) -> str:
        return f"CoinbaseTradingModel(id={self.id!r}, key={self.api_key!r})"


@event.listens_for(CoinbaseTradingModel.__table__, 'after_create')
def create_record(*args, **kwargs):
    session.execute(insert(CoinbaseTradingModel).values())
    session.commit()
    session.close()
