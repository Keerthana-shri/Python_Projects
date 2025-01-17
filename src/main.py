from fastapi import FastAPI
from pydantic import ValidationError
# from src.exceptions.custom_exceptions import custom_validation_exception_handler
from src.utils.init_db import initialize_database
from src.router.api import api_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    initialize_database()

# app.add_exception_handler(ValidationError, custom_validation_exception_handler)

app.include_router(api_router)

# from fastapi import FastAPI
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# from starlette.requests import Request
# from src.utils.init_db import initialize_database
# from src.router.api import api_router

# app = FastAPI()

# templates = Jinja2Templates(directory="templates")

# @app.on_event("startup")
# async def startup_event():
#     initialize_database()

# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# app.include_router(api_router)


