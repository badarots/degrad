from datetime import datetime
from ormar import Model, NoMatch
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyQuery

from app import models
from app.db import Experiment
from app.config import settings
from app.models import BadRequest

API_KEY_NAME = "api_key"
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: str = Security(api_key_query)):
    if api_key == settings.api_key:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )


async def get_experiment(name: str):
    if name == 'null' or name is None:
        return None

    try:
        return await Experiment.objects.get(name=name)
    except NoMatch as e:
        raise NoMatch("No experiment named '{}'".format(name)) from e


async def get_reading(model: Model, params: models.ReadingQuery):
    if params.end is None:
        params.end = datetime.utcnow()

    # also load experiment data
    query = model.objects.select_related(model.experiment).filter(
        (model.date >= params.start) & (model.date <= params.end))

    if params.experiment != 'all':
        query = query.filter(experiment=await get_experiment(params.experiment))

    return await query.limit(params.limit).all()


async def save_reading(reading: Model):
    if reading.experiment is not None:
        if reading.experiment.name == 'all':
            raise BadRequest("'all' is not allowed as an experiment name")

        try:
            reading.experiment = await get_experiment(reading.experiment.name)
        # create a new experiment if it dont exist
        except NoMatch:
            experiment = Experiment(name=reading.experiment.name)
            await experiment.save()
            reading.experiment = experiment

    await reading.save()
    return reading


async def delete_reading(model: Model, params: models.ReadingQuery):
    query = model.objects.filter(
        (model.date >= params.start) & (model.date <= params.end))

    if params.experiment != 'all':
        query = query.filter(experiment=await get_experiment(params.experiment))

    readings = await query.limit(params.limit).all()
    await query.delete()

    return {"deleted_readings": readings}
