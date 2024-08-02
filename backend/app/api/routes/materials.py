import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Material, MaterialCreate, MaterialPublic, MaterialsPublic, MaterialUpdate, Message

router = APIRouter()


@router.get("/", response_model=MaterialsPublic)
def read_materials(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve softwares.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Material)
        count = session.exec(count_statement).one()
        statement = select(Material).offset(skip).limit(limit)
        materials = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Material)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Material)
            .offset(skip)
            .limit(limit)
        )
        materials = session.exec(statement).all()

    material_list: list[MaterialPublic] = []
    for material in materials:
        material_list.append(MaterialPublic(name=material.name,id=material.id))

    return MaterialsPublic(data=material_list, count=count)


@router.get("/{id}", response_model=Material)
def read_material(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get material by ID.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    material = session.get(Material, id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


@router.post("/", response_model=Material)
def create_material(
    *, session: SessionDep, current_user: CurrentUser, material_in: MaterialCreate
) -> Any:
    """
    Create new material.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    material = Material.model_validate(Material(name=material_in.name,id=str(uuid.uuid4())))
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    session.add(material)
    session.commit()
    session.refresh(material)
    return material


@router.put("/{id}", response_model=Material)
def update_material(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    material_in: MaterialUpdate,
) -> Any:
    """
    Update an material.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    material = session.get(Material, id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    update_dict = material_in.model_dump(exclude_unset=True)
    material.sqlmodel_update(update_dict)
    session.add(material)
    session.commit()
    session.refresh(material)
    return material


@router.delete("/{id}")
def delete_material(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an material.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    material = session.get(Material, id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    session.delete(material)
    session.commit()
    return Message(message="Material deleted successfully")