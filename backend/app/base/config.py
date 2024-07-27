import secrets
import warnings
import os 
from typing import Annotated, Any, Literal

from fastapi import FastAPI
from pydantic_settings import BaseSettings # type: ignore
from pydantic import (
    HttpUrl,
    PostgresDsn,
    computed_field
)
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):

    DB_TYPE: str = "sqlite"
    DB_URL: str

    def __init__(self):
        if self.DB_TYPE == "postgresql":
            DB_URL = self.SQLALCHEMY_DATABASE_URI()

    API_STR: str = "/api/v1"
    APP_NAME: str = "SimMat"

    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    if DB_TYPE == "sqlite":
        DB_USER: str = os.getenv("DB_USER","sqlite")
        DB_PORT: int = int(os.getenv("DB_PORT",5432))
        DB_SERVER: str = os.getenv("DB_SERVER","db")
        DB_PASSWORD: str = os.getenv("DB_PASSWORD","")
        DB_NAME: str = os.getenv("DB_NAME","app")
        DB_URL = f"sqlite:///./test.db" #sqlite uses a file as db
    elif DB_TYPE == "postgresql":
        DB_USER: str = os.getenv("DB_USER","postgres")
        DB_PORT: int = int(os.getenv("DB_PORT",5432))
        DB_SERVER: str = os.getenv("DB_SERVER","db")
        DB_PASSWORD: str = os.getenv("DB_PASSWORD","")
        DB_NAME: str = os.getenv("DB_NAME","app")

        @computed_field  # type: ignore[misc]
        @property
        def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
            return MultiHostUrl.build(
                scheme="postgresql+psycopg",
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_SERVER,
                port=self.DB_PORT,
                path=self.DB_NAME,
            )

settings = Settings()  # type: ignore