from fastapi import APIRouter

from app.api.routes import softwares, materials, login, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(materials.router, prefix="/materials", tags=["materials"])
api_router.include_router(softwares.router, prefix="/softwares", tags=["softwares"])