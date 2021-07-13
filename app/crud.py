from datetime import datetime
from ormar import Model

from . import models
from .db import Experiment


async def get_reading(model: Model, params: models.ReadingQuery):
    if params.end is None:
        params.end = datetime.now()
    query = model.objects.select_related(model.experiment).filter(
        (params.start <= model.date) & (model.date <= params.end))
    if params.experiment is not None:
        query = query.filter(experiment__name=params.experiment)

    return await query.limit(params.limit).all()


async def save_reading(reading: Model):
    print(reading)
    if reading.experiment is None:
        # set to the default experiment using its primary key = 1
        reading.experiment = 1
    else:
        experiment = await Experiment.objects.get(name=reading.experiment.name)
        reading.experiment = experiment
    await reading.save()
    return reading


async def delete_reading(model: Model, params: models.ReadingQuery):
    query = await model.objects.filter((params.start <= model.date) & (model.date <= params.end))
    if params.experiment is not None:
        query = query.filter(experiment__name=params.experiment).delete()

    counts = await query.delete()
    return {"deleted_readings": counts}
