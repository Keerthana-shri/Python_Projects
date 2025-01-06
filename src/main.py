from fastapi import FastAPI
from pydantic import ValidationError
# from src.exceptions.custom_exceptions import custom_validation_exception_handler
from src.utils.init_db import initialize_database
from src.router.api import api_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await initialize_database()

# app.add_exception_handler(ValidationError, custom_validation_exception_handler)

app.include_router(api_router)


