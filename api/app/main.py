# app/main.py

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey
from typing import List
from ormar import NoMatch

from app.db import database, Whether, Experiment
from . import crud, models
from app.config import settings

app = FastAPI(title="DegradAPI", root_path=settings.root_path)


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.exception_handler(NoMatch)
async def nomatch_exception_handler(request: Request, exception: NoMatch):
    msg = "Item not found"
    if exception.args:
        msg += ". {}".format(exception)

    return JSONResponse(status_code=404, content={"message": msg})


@app.exception_handler(models.BadRequest)
async def valueerror_exception_handler(request: Request, exception: models.BadRequest):
    msg = "Invalid arguments"
    if exception.args:
        msg += ". {}".format(exception)

    return JSONResponse(status_code=400, content={"message": msg})


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/experiment", response_model=List[Experiment])
async def get_experiments(api_key: APIKey = Depends(crud.get_api_key)):
    return await Experiment.objects.fields(['id', 'name']).all()


@app.post("/experiment", response_model=Experiment)
async def add_experiment(experiment: Experiment, api_key: APIKey = Depends(crud.get_api_key)):
    if experiment.name == 'all':
        raise ValueError("'all' is not allowed as an experiment name")
    return await experiment.save()


@app.delete("/experiment")
async def delete_experiment(name: str, api_key: APIKey = Depends(crud.get_api_key)):
    experiments = await Experiment.objects.get(name=name)
    await experiments.delete()
    return {"deleted_experiments": experiments}


@app.get("/reading/whether", response_model=List[Whether], response_model_exclude={"id", "experiment__id"})
async def get_whether(query: models.ReadingQuery = Depends(), api_key: APIKey = Depends(crud.get_api_key)):
    return await crud.get_reading(Whether, query)


@app.post("/reading/whether", response_model=Whether)
async def add_whether(reading: Whether, api_key: APIKey = Depends(crud.get_api_key)):
    return await crud.save_reading(reading)


@app.delete("/reading/whether")
async def delete_whether(query: models.ReadingQuery = Depends(), api_key: APIKey = Depends(crud.get_api_key)):
    return await crud.delete_reading(Whether, query)
