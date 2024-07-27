from sqlmodel import Session, create_engine, select # type: ignore

from app import crud
from app.base.config import settings
from app.models import User, UserCreate

engine = create_engine(str(settings.DB_URL))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    pass