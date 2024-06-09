from datetime import datetime, timezone
from typing import List

from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyQuery
from sqlalchemy import select, delete

from . import models
from .database import Base, session_maker
from .config import settings

API_KEY_NAME = "api_key"
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: str = Security(api_key_query)):
    if api_key == settings.api_key:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )


async def get_collections() -> List[str]:
    async with session_maker() as session:
        async with session.begin():
            query = select(Base.collection).distinct()
            return (await session.execute(query)).all()


async def query_readings(statement, model: Base, params: models.ReadingQuery):
    if params.end is None:
        params.end = datetime.now(timezone.utc)

    async with session_maker() as session:
        async with session.begin():
            query = statement(model).where(model.time >= params.start).where(model.time <= params.end).limit(params.limit)

            if params.collection != 'all':
                query = query.where(model.collection == params.collection)

            return await session.scalars(query)


async def get_reading(model: Base, params: models.ReadingQuery):
    readings = await query_readings(select, model, params)
    return readings.all()


async def delete_reading(model: Base, params: models.ReadingQuery) -> List[Base]:
    readings = await query_readings(delete, model, params)
    return readings.all()


async def save_reading(model: Base, reading: models.Reading) -> Base:
    if reading.collection == 'all':
        raise models.BadRequest("'all' is not allowed as a collection name")

    async with session_maker() as session:
        async with session.begin():
            db_reading = model(**reading.model_dump())
            session.add(db_reading)

    return db_reading
