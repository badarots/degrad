from fastapi import FastAPI, Depends
from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/reading/temperature", response_model=schemas.Temperature)
def add_temperature(reading: schemas.TemperatureCreate, db: Session = Depends(get_db)):
    return crud.create_temperature(db, temp=reading)


@app.delete("/reading/temperature")
def delete_temperature(start: datetime, end: datetime, db: Session = Depends(get_db)):
    return crud.delete_temperatures(db, start, end)


@app.get("/reading/temperature", response_model=List[schemas.Temperature])
def get_temperature(start: datetime, end: Optional[datetime], limit: int = 100, db: Session = Depends(get_db)):
    if end is None:
        end = datetime.now()
    temps = crud.get_temperatures(db, start=start, end=end, limit=limit)
    return temps
