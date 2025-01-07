from fastapi import FastAPI
from src.utils.init_db import initialize_database
from src.router.api import api_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await initialize_database()

app.include_router(api_router)


