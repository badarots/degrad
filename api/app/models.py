import typing
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.config import settings


class ReadingQuery(BaseModel):
    start: datetime
    end: Optional[datetime]
    experiment: Optional[str] = None
    limit: int = 1000

