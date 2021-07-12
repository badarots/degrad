# app/db.py

import databases
import ormar
import sqlalchemy
from datetime import datetime

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Whether(ormar.Model):
    class Meta(BaseMeta):
        tablename = "whether"

    date = ormar.DateTime(primary_key=True, index=True, default=datetime.now)
    temperature = ormar.Float()
    pressure = ormar.Float(nullable=True)
    humidity = ormar.Float(nullable=True)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
