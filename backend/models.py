from sqlalchemy import Column, Float, Integer, DateTime
from datetime import datetime

from .database import Base


class Whether(Base):
    __tablename__ = "whether"
    date = Column(DateTime, primary_key=True, index=True, default=datetime.now)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
