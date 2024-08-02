import pgserver

import os
dir = os.path.dirname(__file__)
filename = os.path.join(dir, 'pg_data')

test_db = pgserver.get_server(pgdata=filename,cleanup_mode=None) # type: ignore

from pydantic_core import MultiHostUrl
from pydantic import PostgresDsn

from sqlmodel import Session, create_engine, select, SQLModel

def SQLALCHEMY_DATABASE_URI() -> PostgresDsn:
    return MultiHostUrl.build(
        scheme="postgresql+psycopg",
        username="postgres",
        password="password",
        host="localhost",
        port=5432,
        path="db",
    )

engine = create_engine(str(SQLALCHEMY_DATABASE_URI()))

