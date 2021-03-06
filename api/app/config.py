# app/config.py
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    # db_url: str = "sqlite:///./degrad.db"
    root_path: str = Field(..., env='API_PATH')
    api_key: str = Field("secret", env='API_KEY')


settings = Settings()
