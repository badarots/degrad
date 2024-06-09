from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional


class ReadingQuery(BaseModel):
    start: datetime
    # default_factory=datetime.now dont work with fastapi:
    # https://github.com/tiangolo/fastapi/discussions/6123
    end: Optional[datetime] = None
    collection: Optional[str] = 'all'
    limit: int = 1000


class Reading(BaseModel):
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    collection: Optional[str] = None
    info: Optional[str] = None

    class Config:
        from_attributes = True


class Weather(Reading):
    temperature: float
    pressure: Optional[float] = None
    humidity: Optional[float] = None


# custom handled error
class BadRequest(ValueError):
    pass
