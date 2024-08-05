from typing import Any, List

from sqlmodel import Session, select # type: ignore

from app.base.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate
from app.models import Material, MaterialCreate, MaterialUpdate
from app.models import Simulation_Software, Simulation_SoftwareCreate, Simulation_SoftwareUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_material(*, session: Session, material_create: Material) -> Material:
    db_obj = Material.model_validate(material_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_material(*,session:Session, db_material: Material, material_in: MaterialUpdate) -> Any:
    material_data = material_in.model_dump(exclude_unset=True)
    db_material.sqlmodel_update(material_data)
    session.add(db_material)
    session.commit()
    session.refresh(db_material)
    return db_material

def get_material_by_name(*,session:Session, db_material: Material, name: str) -> Material | None:
    statement = select(Material).where(Material.name == name)
    session_material = session.exec(statement).first()
    return session_material


def create_simulation_software(*, session: Session, simulation_software_create: Simulation_SoftwareCreate) -> Simulation_Software:
    db_obj = Simulation_Software.model_validate(simulation_software_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_simulation_software(*,session:Session, db_simulation_software: Simulation_Software, simulation_software_in: Simulation_SoftwareUpdate) -> Any:
    simulation_software_data = simulation_software_in.model_dump(exclude_unset=True)
    db_simulation_software.sqlmodel_update(simulation_software_data)
    session.add(db_simulation_software)
    session.commit()
    session.refresh(db_simulation_software)
    return db_simulation_software

def get_simulation_software_by_name(*,session:Session, db_simulation_software: Simulation_Software, name: str) -> Simulation_Software | None:
    statement = select(Simulation_Software).where(Simulation_Software.name == name)
    session_simulation_software = session.exec(statement).first()
    return session_simulation_software

