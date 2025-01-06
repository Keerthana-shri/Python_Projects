from fastapi import APIRouter
from src.router.v1 import pokemon

api_router = APIRouter()
api_router.include_router(pokemon.router, prefix="/v1", tags=["pokemon"])

# from fastapi import APIRouter
# from src.router.v1 import pokemon

# api_router = APIRouter()
# api_router.include_router(pokemon.router, prefix="/v1", tags=["pokemon"])
