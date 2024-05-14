from sqlalchemy import Boolean, insert, event, Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from environs import Env

from src.database.mydb import session, Base

env = Env()
env.read_env()

YAHOO_FINANCE_TABLE_NAME = "yahoo_finance"
YAHOO_FINANCE_ENDPOINT = env.str("YAHOO_FINANCE_ENDPOINT", "https://query1.finance.yahoo.com/v7/finance/download/")


class YahooFinanceModel(Base):
    __tablename__ = YAHOO_FINANCE_TABLE_NAME

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    endpoint: Mapped[str] = mapped_column(String(255), default=YAHOO_FINANCE_ENDPOINT)
    is_active: Mapped[bool] = mapped_column(Boolean(), unique=False, default=True)

    def __repr__(self) -> str:
        return f"YahooFinanceModel(id={self.id!r}, key={self.endpoint!r})"


@event.listens_for(YahooFinanceModel.__table__, 'after_create')
def create_record(*args, **kwargs):
    session.execute(insert(YahooFinanceModel).values())
    session.commit()
    session.close()
