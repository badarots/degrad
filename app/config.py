# app/config.py

# import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # db_url: str = Field(..., env='DATABASE_URL')
    db_url: str = "sqlite:///./degrad.db"
    default_experiment: str = 'test'

settings = Settings()
