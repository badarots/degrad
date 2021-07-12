# app/main.py

from fastapi import FastAPI
from typing import Optional, List
from datetime import datetime

from app.db import database, Whether
from . import crud


app = FastAPI(title="DegradAPI")


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/reading/whether", response_model=List[Whether])
async def get_whether(start: datetime, end: Optional[datetime] = None, limit: int = 1000):
    if end is None:
        end = datetime.now()
    return await crud.get_reading(Whether, start=start, end=end, limit=limit)


@app.post("/reading/whether", response_model=Whether)
async def add_whether(reading: Whether):
    return await crud.save_reading(reading)


@app.delete("/reading/whether")
async def delete_whether(start: datetime, end: datetime):
    return await crud.delete_reading(Whether, start, end)
