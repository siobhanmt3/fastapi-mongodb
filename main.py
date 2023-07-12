from fastapi import FastAPI
from routes import inventory

app = FastAPI()

app.include_router(inventory.router)

@app.get("/healthcheck")
async def healthcheck():
    return{
        "healthcheck" : "Ok"
    }