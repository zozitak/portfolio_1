import secrets
import warnings
import os 
from typing import Annotated, Any, Literal

from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from pydantic import (
    HttpUrl,
    PostgresDsn,
    computed_field,
    Field
)
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    DB_TYPE: str = Field(default="sqlite",validate_default=False)
    DB_URL: str = Field(default="",validate_default=False)

    API_STR: str = "/api/v1"
    APP_NAME: str = "SimMat"

    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    DB_USER: str = Field(default="",validate_default=False)
    DB_PORT: int = Field(default=5432,validate_default=False)
    DB_SERVER: str = Field(default="",validate_default=False)
    DB_PASSWORD: str = Field(default="",validate_default=False)
    DB_NAME: str = Field(default="",validate_default=False)

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

    def get_url(self) -> str:
        if self.DB_TYPE == "sqlite":
            self.DB_USER = os.getenv("DB_USER","sqlite")
            self.DB_PORT = int(os.getenv("DB_PORT",5432))
            self.DB_SERVER = os.getenv("DB_SERVER","db")
            self.DB_PASSWORD = os.getenv("DB_PASSWORD","")
            self.DB_NAME = os.getenv("DB_NAME","app")
            self.DB_URL = f"sqlite:///./test.db" #sqlite uses a file as db
            return self.DB_URL
        elif self.DB_TYPE == "postgresql":
            self.DB_USER = os.getenv("DB_USER","postgres")
            self.DB_PORT = int(os.getenv("DB_PORT",5432))
            self.DB_SERVER = os.getenv("DB_SERVER","db")
            self.DB_PASSWORD = os.getenv("DB_PASSWORD","")
            self.DB_NAME = os.getenv("DB_NAME","app")
            self.DB_URL = self.SQLALCHEMY_DATABASE_URI()
            return self.DB_URL

settings = Settings()  # type: ignore