from fastapi import APIRouter,status,Response

router = APIRouter()

@router.get("/",status_code=status.HTTP_204_NO_CONTENT)
def users():
    return Response(status_code=status.HTTP_204_NO_CONTENT)