from sqlalchemy import Boolean, insert, event, Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from environs import Env

from src.database.mydb import session, Base

env = Env()
env.read_env()

POLYGON_TABLE_NAME = "polygon"
POLYGON_API_KEY = env.str("POLYGON_API_KEY", "nada")
POLYGON_ENDPOINT = env.str("POLYGON_ENDPOINT", "nada")


class PolygonIoModel(Base):
    __tablename__ = POLYGON_TABLE_NAME

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    api_key: Mapped[str] = mapped_column(String(255), default=POLYGON_API_KEY)
    endpoint: Mapped[str] = mapped_column(String(255), default=POLYGON_ENDPOINT)
    active: Mapped[bool] = mapped_column(Boolean(), unique=False, default=True)

    def __repr__(self) -> str:
        return f"PolygonModel(id={self.id!r}, key={self.api_key!r})"


@event.listens_for(PolygonIoModel.__table__, 'after_create')
def create_record(*args, **kwargs):
    session.execute(insert(PolygonIoModel).values())
    session.commit()
    session.close()
