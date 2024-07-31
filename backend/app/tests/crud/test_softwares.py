from fastapi.encoders import jsonable_encoder
from sqlmodel import Session  # type: ignore

from app import crud
from app.base.security import verify_password
from app.models import User, UserCreate, UserUpdate
from app.models import Material, MaterialCreate, MaterialUpdate
from app.models import Simulation_Software, Simulation_SoftwareCreate, Simulation_SoftwareUpdate
from app.tests.utils.utils import random_email, random_lower_string

def test_create_simulation_software(db: Session) -> None:
    simulation_software_name = random_lower_string()
    simulation_software_in = Simulation_SoftwareCreate(name=simulation_software_name,description="test")
    simulation_software = crud.create_simulation_software(session=db,simulation_software_create=simulation_software_in)
    assert simulation_software.name == simulation_software_name

def test_update_simulation_software(db: Session) -> None:
    simulation_software_name = random_lower_string()
    simulation_software_in = Simulation_SoftwareCreate(name=simulation_software_name,description="test")
    simulation_software = crud.create_simulation_software(session=db,simulation_software_create=simulation_software_in)
    simulation_software_desc_update = random_lower_string()
    simulation_software_in_update = Simulation_SoftwareUpdate(description=simulation_software_desc_update)
    if simulation_software.id is not None:
        crud.update_simulation_software(session=db, db_simulation_software=simulation_software, simulation_software_in=simulation_software_in_update)
    simulation_software_updated_desc = db.get(Simulation_Software, simulation_software.id)
    assert simulation_software_updated_desc.description == simulation_software_desc_update
    assert simulation_software_updated_desc != simulation_software.description
    
def test_get_simulation_software(db: Session) -> None:
    simulation_software_name = random_lower_string()
    print(simulation_software_name)
    simulation_software_in = Simulation_SoftwareCreate(name=simulation_software_name,description="test")
    simulation_software = crud.create_simulation_software(session=db,simulation_software_create=simulation_software_in)
    if simulation_software.id is not None:
        simulation_software_got = crud.get_simulation_software_by_name(session=db, db_simulation_software=simulation_software, name=simulation_software.name)
        print(simulation_software.name)
    assert simulation_software_got.name == simulation_software.name
    assert jsonable_encoder(simulation_software_got)