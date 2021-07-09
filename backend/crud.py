from sqlalchemy import delete
from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas


def push_to_db(db: Session, entry):
    db.add(entry)
    db.commit()
    db.refresh(entry)


def get_temperature(db: Session, temp_id: int):
    db.delete()
    return db.query(models.Temperature).filter(models.Temperature.id == temp_id).first()


def get_temperatures(db: Session, start: datetime, end: datetime, limit: int = 100):
    return db.query(models.Temperature)\
        .filter(models.Temperature.date >= start, models.Temperature.date <= end)\
        .limit(limit).all()


def create_temperature(db: Session, temp: schemas.TemperatureCreate):
    db_temp = models.Temperature(**temp.dict())
    push_to_db(db, db_temp)
    return db_temp


def delete_temperatures(db: Session, start: datetime, end: datetime):
    count = db.query(models.Temperature)\
        .filter(models.Temperature.date >= start, models.Temperature.date <= end)\
        .delete()
    db.commit()
    return count
