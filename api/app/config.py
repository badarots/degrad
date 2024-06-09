# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres@localhost:5432/degrad"
    api_path: str = ""
    api_key: str = "secret"


settings = Settings()
