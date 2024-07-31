from fastapi.encoders import jsonable_encoder
from sqlmodel import Session  # type: ignore

from app import crud
from app.base.security import verify_password
from app.models import User, UserCreate, UserUpdate
from app.models import Material, MaterialCreate, MaterialUpdate
from app.models import Simulation_Software, Simulation_SoftwareCreate, Simulation_SoftwareUpdate
from app.tests.utils.utils import random_email, random_lower_string

def test_create_material(db: Session) -> None:
    material_name = random_lower_string()
    material_in = MaterialCreate(name=material_name,description="test")
    material = crud.create_material(session=db,material_create=material_in)
    assert material.name == material_name

def test_update_material(db: Session) -> None:
    material_name = random_lower_string()
    material_in = MaterialCreate(name=material_name,description="test")
    material = crud.create_material(session=db,material_create=material_in)
    matraial_desc_update = random_lower_string()
    material_in_update = MaterialUpdate(description=matraial_desc_update)
    if material.id is not None:
        crud.update_material(session=db, db_material=material, material_in=material_in_update)
    material_updated_desc = db.get(Material, material.id)
    assert material_updated_desc.description == matraial_desc_update
    assert material_updated_desc != material.description
    
def test_get_material(db: Session) -> None:
    material_name = random_lower_string()
    material_in = MaterialCreate(name=material_name,description="test")
    material = crud.create_material(session=db,material_create=material_in)
    if material.id is not None:
        material_got = crud.get_material_by_name(session=db, db_material=material, name=material_name)
    assert material_got.name == material.name
    assert jsonable_encoder(material_got)

