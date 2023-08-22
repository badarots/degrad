from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReadingQuery(BaseModel):
    start: datetime
    # default_factory=datetime.now dont work with fastapi:
    # https://github.com/tiangolo/fastapi/discussions/6123
    end: Optional[datetime] = None
    experiment: Optional[str] = 'all'
    limit: int = 1000


# custon handled error
class BadRequest(ValueError):
    pass
