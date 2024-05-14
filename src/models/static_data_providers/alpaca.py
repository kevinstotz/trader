from sqlalchemy import Boolean, insert, event, Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from environs import Env

from src.database.mydb import session, Base

env = Env()
env.read_env()

ALPACA_TABLE_NAME = "alpaca"
ALPACA_API_KEY = env.str("ALPACA_API_KEY", "nada")
ALPACA_SECRET_KEY = env.str("ALPACA_SECRET_KEY", "nada")
ALPACA_ENDPOINT = env.str("ALPACA_ENDPOINT", "nada")


class AlpacaModel(Base):
    __tablename__ = ALPACA_TABLE_NAME

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    api_key: Mapped[str] = mapped_column(String(255), default=ALPACA_API_KEY)
    api_secret: Mapped[str] = mapped_column(String(255), default=ALPACA_SECRET_KEY)
    active: Mapped[bool] = mapped_column(Boolean(), unique=False, default=True)

    def __repr__(self) -> str:
        return f"AlpacaModel(id={self.id!r}, key={self.api_key!r})"


@event.listens_for(AlpacaModel.__table__, 'after_create')
def create_record(*args, **kwargs):
    session.execute(insert(AlpacaModel).values())
    session.commit()
    session.close()
