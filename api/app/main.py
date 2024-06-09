# app/main.py

from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security.api_key import APIKey

from . import crud, models, database
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await database.engine.dispose()


app = FastAPI(title="DegradAPI", root_path=settings.api_path, lifespan=lifespan)


@app.exception_handler(models.BadRequest)
async def valueerror_exception_handler(request: Request, exception: models.BadRequest):
    msg = "Invalid arguments"
    if exception.args:
        msg += ". {}".format(exception)

    return JSONResponse(status_code=400, content={"message": msg})


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse(settings.api_path + "/docs")


@app.get("/collections", response_model=List[str])
async def get_collections(api_key: APIKey = Depends(crud.get_api_key)):
    return await crud.get_collections()


@app.get("/reading/weather", response_model=list[models.Weather])
async def get_whether(query: models.ReadingQuery = Depends(), api_key: APIKey = Depends(crud.get_api_key)):
    return await crud.get_reading(database.Weather, query)


@app.delete("/reading/weather", response_model=List[models.Weather])
async def delete_whether(query: models.ReadingQuery = Depends(), api_key: APIKey = Depends(crud.get_api_key)):
    return await crud.delete_reading(database.Weather, query)


@app.post("/reading/weather", response_model=models.Weather)
async def add_whether(reading: models.Weather, api_key: APIKey = Depends(crud.get_api_key)):
    return await crud.save_reading(database.Weather, reading)
