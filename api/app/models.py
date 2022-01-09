from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReadingQuery(BaseModel):
    start: datetime
    # FIXME: default_factory=datetime.now não funcionou por algum motivo
    end: Optional[datetime] = None
    experiment: Optional[str] = 'all'
    limit: int = 1000


# custon handled error
class BadRequest(ValueError):
    pass
