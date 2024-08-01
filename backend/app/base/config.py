import secrets
import warnings
import os
from typing import Annotated, Any, Literal

from psycopg import NotSupportedError
from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
    Field
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from typing_extensions import Self 

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    DB_TYPE: str = Field(default="postgresql",validate_default=False)
    DB_URL: str = Field(default="",validate_default=False)

    API_STR: str = "/api/v1"
    APP_NAME: str = "SimMat"
    OPERATION_MODE: str = "unittest"

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"
    
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    PROJECT_NAME: str = Field(default="SimMat",validate_default=False)
    DB_USER: str = Field(default="",validate_default=False)
    DB_PORT: int = Field(default=5432,validate_default=False)
    DB_SERVER: str = Field(default="",validate_default=False)
    DB_PASSWORD: str = Field(default="",validate_default=False)
    DB_NAME: str = Field(default="",validate_default=False)

    def get_url(self) -> str:
        if self.DB_TYPE == "sqlite":
            self.DB_USER = os.getenv("DB_USER","sqlite")
            self.DB_PORT = int(os.getenv("DB_PORT",5432))
            self.DB_SERVER = os.getenv("DB_SERVER","localhost")
            self.DB_PASSWORD = os.getenv("DB_PASSWORD","")
            self.DB_NAME = os.getenv("DB_NAME","app")
            self.DB_URL = f"sqlite:///./test.db" #sqlite uses a file as db
            return self.DB_URL
        elif self.DB_TYPE == "postgresql":
            self.DB_USER = os.getenv("DB_USER","postgres")
            self.DB_PORT = int(os.getenv("DB_PORT",5432))
            self.DB_SERVER = os.getenv("DB_SERVER","localhost")
            self.DB_PASSWORD = os.getenv("DB_PASSWORD","password")
            self.DB_NAME = os.getenv("DB_NAME","app")
            self.DB_URL = str(self.SQLALCHEMY_DATABASE_URI)
            return self.DB_URL
        else:
            raise NotSupportedError
        
    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_SERVER,
            port=self.DB_PORT,
            path=self.DB_NAME
        )
    
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    EMAIL_TEST_USER: str = Field(default="test@example.com",validate_default=False)
    FIRST_USER: str = Field(default="test",validate_default=False)
    FIRST_USER_PASSWORD: str = Field(default="securepassword2",validate_default=False)
    
    EMAIL_TEST_SUPER_USER: str = Field(default="supertest@example.com",validate_default=False)
    FIRST_SUPERUSER: str = Field(default="supertest",validate_default=False)
    FIRST_SUPERUSER_PASSWORD: str = Field(default="supersecurepassword2",validate_default=False)

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)
            
    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("DB_PASSWORD", self.DB_PASSWORD)
        self._check_default_secret("FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD)
        return self

settings = Settings()  # type: ignore