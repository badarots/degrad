from datetime import datetime
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyQuery

from app import models
from app.db import Experiment
from app.config import settings

API_KEY_NAME = "api_key"
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: str = Security(api_key_query)):
    if api_key == settings.api_key:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZE,
        detail="Could not validate credentials"
    )


async def get_reading(model: Model, params: models.ReadingQuery):
    if params.end is None:
        params.end = datetime.now()
    query = model.objects.select_related(model.experiment).filter(
        (params.start <= model.date) & (model.date <= params.end))
    if params.experiment != 'all':
        query = query.filter(experiment__name=params.experiment)

    return await query.limit(params.limit).all()


async def save_reading(reading: Model):
    if reading.experiment == 'all':
        raise ValueError("'all' is not allowed as an experiment name")
    
    if reading.experiment is not None:
        experiment = await Experiment.objects.get(name=reading.experiment.name)
        reading.experiment = experiment

    await reading.save()
    return reading


async def delete_reading(model: Model, params: models.ReadingQuery):
    query = await model.objects.filter((params.start <= model.date) & (model.date <= params.end))
    if params.experiment != 'all':
        query = query.filter(experiment__name=params.experiment).delete()

    counts = await query.delete()
    return {"deleted_readings": counts}
