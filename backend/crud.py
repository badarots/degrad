from sqlalchemy import delete
from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas


def push_to_db(db: Session, entry):
    db.add(entry)
    db.commit()
    db.refresh(entry)


def get_whether(db: Session, start: datetime, end: datetime, limit: int = 100):
    return db.query(models.Whether)\
        .filter(models.Whether.date >= start, models.Whether.date <= end)\
        .limit(limit).all()


def create_whether(db: Session, temp: schemas.WhetherCreate):
    db_temp = models.Whether(**temp.dict())
    push_to_db(db, db_temp)
    return db_temp


def delete_whether(db: Session, start: datetime, end: datetime):
    count = db.query(models.Whether)\
        .filter(models.Whether.date >= start, models.Whether.date <= end)\
        .delete()
    db.commit()
    return count
