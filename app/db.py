# app/db.py

import databases
import ormar
import sqlalchemy
from datetime import datetime
from typing import Optional, Union

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Experiment(ormar.Model):
    class Meta(BaseMeta):
        tablename = "experiment"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, unique=True)


class Whether(ormar.Model):
    class Meta(BaseMeta):
        tablename = "whether"

    date: datetime = ormar.DateTime(
        primary_key=True, index=True, default=datetime.now, unique=False)
    temperature: float = ormar.Float()
    pressure: float = ormar.Float(nullable=True)
    humidity: float = ormar.Float(nullable=True)
    experiment: Optional[Experiment] = ormar.ForeignKey(
        Experiment, skip_reverse=True)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
