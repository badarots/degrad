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


@app.get("/reading/whether", response_model=List[schemas.Whether])
def get_whether(start: datetime, end: Optional[datetime] = None, limit: int = 100, db: Session = Depends(get_db)):
    if end is None:
        end = datetime.now()
    temps = crud.get_whether(db, start=start, end=end, limit=limit)
    return temps


@app.post("/reading/whether", response_model=schemas.Whether)
def add_whether(reading: schemas.WhetherCreate, db: Session = Depends(get_db)):
    return crud.create_whether(db, temp=reading)


@app.delete("/reading/whether")
def delete_whether(start: datetime, end: datetime, db: Session = Depends(get_db)):
    return crud.delete_whether(db, start, end)
