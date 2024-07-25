from fastapi import FastAPI

app = FastAPI(title="SimMat")


@app.get("/")
async def root():
    return {"msg": "Hello World"}