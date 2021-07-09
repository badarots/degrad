from sqlalchemy import Column, Float, Integer, DateTime
from datetime import datetime

from .database import Base


class Temperature(Base):

    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, unique=True, index=True, default=datetime.now)
    value = Column(Float)
