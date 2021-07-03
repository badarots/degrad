from pydantic import BaseModel
from datetime import date, datetime


class SingleReading(BaseModel):
    date: datetime
    value: float


class Playload:
    hash: str = "hash"


class TemperatureBase(SingleReading):
    pass


class TemperatureCreate(TemperatureBase, Playload):
    pass


class Temperature(TemperatureBase, Playload):
    class Config:
        orm_mode = True
