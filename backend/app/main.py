from fastapi import FastAPI, status, Response

app = FastAPI(title="SimMat")


@app.get("/",status_code=status.HTTP_204_NO_CONTENT)
async def root():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

