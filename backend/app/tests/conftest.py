from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete # type: ignore

from app.base.config import settings
from app.base.db import engine, init_db
from app.main import app
from app.models import Material, Simulation_Software, User


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        # statement = delete(Material)
        # session.execute(statement)
        # statement = delete(Simulation_Software)
        # session.execute(statement)
        # statement = delete(User)
        # session.execute(statement)
        # session.commit()