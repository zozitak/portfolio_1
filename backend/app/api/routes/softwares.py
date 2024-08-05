import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Simulation_Software, Simulation_SoftwareCreate, Simulation_SoftwarePublic, Simulation_SoftwaresPublic, Simulation_SoftwareUpdate, Message

router = APIRouter()


@router.get("/", response_model=Simulation_SoftwaresPublic)
def read_softwares(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve softwares.
    """

    count_statement = (
        select(func.count())
        .select_from(Simulation_Software)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Simulation_Software)
        .offset(skip)
        .limit(limit)
    )
    softwares = session.exec(statement).all()

    software_list: list[Simulation_SoftwarePublic] = []
    for software in softwares:
        software_list.append(Simulation_SoftwarePublic(name=software.name,id=software.id))

    return Simulation_SoftwaresPublic(data=software_list, count=count)


@router.get("/{id}", response_model=Simulation_Software)
def read_software(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get software by ID.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    software = session.get(Simulation_Software, id)
    if not software:
        raise HTTPException(status_code=404, detail="Software not found")
    return software


@router.post("/", response_model=Simulation_Software)
def create_software(
    *, session: SessionDep, current_user: CurrentUser, software_in: Simulation_SoftwareCreate
) -> Any:
    """
    Create new software.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    software = Simulation_Software.model_validate(Simulation_Software(name=software_in.name,id=str(uuid.uuid4())))
    if not software:
        raise HTTPException(status_code=404, detail="Software not found")
    session.add(software)
    session.commit()
    session.refresh(software)
    return software


@router.put("/{id}", response_model=Simulation_Software)
def update_software(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    software_in: Simulation_SoftwareUpdate,
) -> Any:
    """
    Update an software.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    software = session.get(Simulation_Software, id)
    if not software:
        raise HTTPException(status_code=404, detail="Software not found")
    update_dict = software_in.model_dump(exclude_unset=True)
    software.sqlmodel_update(update_dict)
    session.add(software)
    session.commit()
    session.refresh(software)
    return software


@router.delete("/{id}")
def delete_software(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an software.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    software = session.get(Simulation_Software, id)
    if not software:
        raise HTTPException(status_code=404, detail="Software not found")
    session.delete(software)
    session.commit()
    return Message(message="Software deleted successfully")