from sqlmodel import Session

from app import crud
from app.models import Simulation_Software, Simulation_SoftwareCreate
from app.tests.utils.utils import random_lower_string


def create_random_software(db: Session) -> Simulation_Software:
    name = random_lower_string()
    description = random_lower_string()
    software_in = Simulation_SoftwareCreate(name=name, description=description)
    return crud.create_simulation_software(session=db, simulation_software_create=software_in)