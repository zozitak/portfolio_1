from typing import Union
from sqlmodel import Session, create_engine, select, delete, SQLModel# type: ignore

from app import crud
from app.base.config import settings
from app.models import User, UserCreate
from app.models import Material, MaterialCreate
from app.models import Simulation_Software, Simulation_SoftwareCreate

engine = create_engine(settings.get_url())

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    #create active super user
    superuser = session.exec(
        select(User).where(User.email == settings.EMAIL_TEST_SUPER_USER)
    ).first()
    if not superuser:
        user_in = UserCreate(
            email=settings.EMAIL_TEST_SUPER_USER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        superuser = crud.create_user(session=session, user_create=user_in)

    #create active normal user
    normaluser = session.exec(
        select(User).where(User.email == settings.EMAIL_TEST_USER)
    ).first()
    if not normaluser:
        user_in = UserCreate(
            email=settings.EMAIL_TEST_USER,
            password=settings.FIRST_USER_PASSWORD,
            is_superuser=False,
        )
        normaluser = crud.create_user(session=session, user_create=user_in)

    #create test material
    testmaterial = session.exec(
        select(Material).where(Material.name == "material")
    ).first()
    if not testmaterial:
        material_in = MaterialCreate(
            name = "material",
        )
        testmaterial = crud.create_material(session=session,material_create=material_in)

    #create test material
    testsoftware = session.exec(
        select(Simulation_Software).where(Simulation_Software.name == "software")
    ).first()
    if not testsoftware:
        software_in = Simulation_SoftwareCreate(
            name = "software",
        )
        testsoftware = crud.create_simulation_software(session=session,simulation_software_create=software_in)


def dest_db(session: Session):
    #search
    statement = select(Material)
    results = session.exec(statement)
    for res in results:
        session.delete(res)
        session.commit()

    statement = select(Simulation_Software)
    results = session.exec(statement)
    for res in results:
        session.delete(res)
        session.commit()

    statement = select(User)
    results = session.exec(statement)
    for res in results:
        session.delete(res)
        session.commit()