from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_STR: str = "/api/v1"
    APP_NAME: str = "SimMat"

settings = Settings()  # type: ignore