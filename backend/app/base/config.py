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

    def __init__(self):
        if self.DB_TYPE == "sqlite":
            self.DB_USER = os.getenv("DB_USER","sqlite")
            self.DB_PORT = int(os.getenv("DB_PORT",5432))
            self.DB_SERVER = os.getenv("DB_SERVER","db")
            self.DB_PASSWORD = os.getenv("DB_PASSWORD","")
            self.DB_NAME = os.getenv("DB_NAME","app")
            self.DB_URL = f"sqlite:///./test.db" #sqlite uses a file as db
        elif self.DB_TYPE == "postgresql":
            self.DB_USER = os.getenv("DB_USER","postgres")
            self.DB_PORT = int(os.getenv("DB_PORT",5432))
            self.DB_SERVER = os.getenv("DB_SERVER","db")
            self.DB_PASSWORD = os.getenv("DB_PASSWORD","")
            self.DB_NAME = os.getenv("DB_NAME","app")
            self.DB_URL = self.SQLALCHEMY_DATABASE_URI()

    DB_TYPE: str = "sqlite" 
    DB_URL: str 

    API_STR: str = "/api/v1"
    APP_NAME: str = "SimMat"

    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    DB_USER: str
    DB_PORT: int
    DB_SERVER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_URL: str

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