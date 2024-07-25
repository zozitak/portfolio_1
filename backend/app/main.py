from fastapi import FastAPI, status, Response

from app.base.config import settings
from app.api.main import api_router

app = FastAPI(title=settings.APP_NAME)

@app.get("/",status_code=status.HTTP_204_NO_CONTENT)
async def root():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

app.include_router(api_router, prefix=settings.API_STR)