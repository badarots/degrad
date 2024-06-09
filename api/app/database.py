from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .config import settings

class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    time: Mapped[datetime] = mapped_column(server_default=func.now())
    collection: Mapped[Optional[str]] = mapped_column(index=True)
    info: Mapped[Optional[str]]


class Weather(Base):
    __tablename__ = "weather"

    temperature: Mapped[float]
    pressure: Mapped[Optional[float]]
    humidity: Mapped[Optional[float]]

engine = create_async_engine(settings.database_url)

session_maker = async_sessionmaker(engine, expire_on_commit=False)
