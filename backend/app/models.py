import uuid

from typing import Dict, Any, List

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, Column, JSON # type: ignore


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)

# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)

class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)

class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class Simulation_SoftwareBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)

# Properties to receive via API on creation
class Simulation_SoftwareCreate(Simulation_SoftwareBase):
    name: str = Field(default=None,min_length=1, max_length=255)

# Properties to receive via API on update, all are optional
class Simulation_SoftwareUpdate(Simulation_SoftwareBase):
    name: str | None = Field(default=None,min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    url: str | None = Field(default=None,min_length=1, max_length=255)

# Database model, database table inferred from class name
class Simulation_Software(Simulation_SoftwareBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=255)
    url: str | None = Field(default=None,min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)

# Properties to return via API, id is always required
class Simulation_SoftwarePublic(Simulation_SoftwareBase):
    id: uuid.UUID

class Simulation_SoftwaresPublic(SQLModel):
    data: list[Simulation_SoftwarePublic]
    count: int


# Shared properties
class MaterialBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)

# Properties to receive via API on creation
class MaterialCreate(MaterialBase):
    description: str | None = Field(default=None, max_length=255)

# Properties to receive via API on update, all are optional
class MaterialUpdate(MaterialBase):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    material_json: Dict[Any, Any] | None = Field(default=None, sa_column=Column(JSON))

# Database model, database table inferred from class name
class Material(MaterialBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    description: str | None = Field(default=None, max_length=255)
    simulation_software_name: str | None = Field(default=None, max_length=255)
    simulation_software_id: uuid.UUID | None = Field(default=None)
    material_json: Dict[Any, Any] | None = Field(default=None,sa_column=Column(JSON))

# Properties to return via API, id is always required
class MaterialPublic(MaterialBase):
    id: uuid.UUID
    description: str | None = Field(default=None, max_length=255)

class MaterialsPublic(SQLModel):
    data: list[MaterialPublic]
    count: int
    

# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)