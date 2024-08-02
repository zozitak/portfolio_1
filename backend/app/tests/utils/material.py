from sqlmodel import Session

from app import crud
from app.models import Material, MaterialCreate
from app.tests.utils.utils import random_lower_string


def create_random_material(db: Session) -> Material:
    name = random_lower_string()
    description = random_lower_string()
    material_in = MaterialCreate(name=name, description=description)
    return crud.create_material(session=db, material_in=material_in)