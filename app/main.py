# app/main.py

from fastapi import FastAPI, Depends
from typing import Optional, List
from datetime import datetime

from app.db import database, Whether, Experiment
from . import crud, models
from .config import settings



app = FastAPI(title="DegradAPI")


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # Create default experiment
    await Experiment.objects.get_or_create(name=settings.default_experiment)


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/experiment", response_model=List[Experiment])
async def get_experiments():
    return await Experiment.objects.fields(['id', 'name']).all()


@app.post("/experiment", response_model=Experiment)
async def add_experiment(experiment: Experiment):
    return await experiment.save()


@app.delete("/experiment")
async def delete_experiment(name: str):
    return await Experiment.objects.delete(name=name)


@app.get("/reading/whether", response_model=List[Whether], response_model_exclude={"experiment__id"})
async def get_whether(query: models.ReadingQuery = Depends()):
    return await crud.get_reading(Whether, query)


@app.post("/reading/whether", response_model=Whether)
async def add_whether(reading: Whether):
    return await crud.save_reading(reading)


@app.delete("/reading/whether")
async def delete_whether(query: models.ReadingQuery = Depends()):
    return await crud.delete_reading(Whether, query)
