from datetime import datetime
from ormar import Model


async def get_reading(model: Model, start: datetime, end: datetime, limit: int = 1000):
    return await model.objects.filter((start <= model.date) & (model.date <= end)).limit(limit).all()


async def save_reading(reading: Model):
    await reading.save()
    return reading


async def delete_reading(model: Model, start: datetime, end: datetime):
    count = await model.objects.filter((start <= model.date) & (model.date <= end)).delete()
    return {"deleted_readings": count}
