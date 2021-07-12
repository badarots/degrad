from pydantic import BaseModel
from datetime import datetime


class Playload:
    hash: str = "hash"


class WhetherBase(BaseModel):
    date: datetime
    temperature: float
    pressure: float
    humidity: float


class WhetherCreate(Playload, WhetherBase):
    pass


class Whether(WhetherBase):
    class Config:
        orm_mode = True
