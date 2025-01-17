from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ValidationError
from src.schemas.pokemon_schema import PokemonInput
from src.service.pokemon_service import PokemonService
from src.config.database import get_db
from src.unit_of_work import UnitOfWork
from typing import Optional, List

router = APIRouter()

def get_pokemon_service(db=Depends(get_db)):
    uow = UnitOfWork()
    service = PokemonService(uow)
    return service

@router.get("/pokemon/id/{pokemon_id}")
async def get_pokemon_by_id(
    pokemon_id: int,
    service: PokemonService = Depends(get_pokemon_service),
):
    pokemon = await service.fetch_pokemon_by_id(pokemon_id)
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

@router.get("/pokemon")
async def get_all_pokemons(
    page: int = 1,
    limit: int = 20,
    name: Optional[str] = None,
    height: Optional[int] = Query(None),
    min_height: Optional[int] = Query(None),
    max_height: Optional[int] = Query(None),
    weight: Optional[int] = Query(None),
    min_weight: Optional[int] = Query(None),
    max_weight: Optional[int] = Query(None),
    xp: Optional[int] = Query(None),
    min_xp: Optional[int] = Query(None),
    max_xp: Optional[int] = Query(None),
    abilities: Optional[List[str]] = Query(None),
    stats: Optional[List[str]] = Query(None),
    types: Optional[List[str]] = Query(None),
    base_stat: Optional[int] = Query(None),
    min_base_stat: Optional[int] = Query(None),
    max_base_stat: Optional[int] = Query(None),
    is_hidden: Optional[bool] = Query(None),
    service: PokemonService = Depends(get_pokemon_service),
):
    return await service.fetch_all_pokemons(
        page, limit, name, height, min_height, max_height, weight, min_weight, max_weight,
        xp, min_xp, max_xp, abilities, stats, types, base_stat, min_base_stat, max_base_stat, is_hidden
    )

@router.post("/pokemon")
async def add_pokemon(
    pokemon_data: PokemonInput,
    service: PokemonService = Depends(get_pokemon_service)
):
    try:
        pokemon_data = PokemonInput(**pokemon_data.dict())
        pokemon_id = await service.create_pokemon(pokemon_data)
        return {"details": "Pokemon added.", "id": pokemon_id}
    except ValidationError as e:
        raise e  # This will be caught by the custom exception handler
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/pokemon/id/{pokemon_id}")
async def update_pokemon_details(
    pokemon_id: int,
    updated_data: PokemonInput,
    service: PokemonService = Depends(get_pokemon_service),
):
    existing_pokemon = await service.fetch_pokemon_by_id(pokemon_id)
    if not existing_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    
    try:
        updated_data = PokemonInput(**updated_data.dict())
        await service.update_pokemon(pokemon_id, updated_data)
        return {"detail": "Pokemon updated successfully"}
    except ValidationError as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/pokemon/id/{pokemon_id}")
async def remove_pokemon(
    pokemon_id: int,
    service: PokemonService = Depends(get_pokemon_service)
):
    pokemon = await service.fetch_pokemon_by_id(pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    
    await service.delete_pokemon(pokemon_id)
    
    return {"detail": "Pokemon deleted"}


# from fastapi import APIRouter, Depends, HTTPException, Query
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# from starlette.requests import Request
# from src.schemas.pokemon_schema import PokemonInput
# from src.service.pokemon_service import PokemonService
# from src.config.database import get_db
# from src.unit_of_work import UnitOfWork
# from typing import Optional, List

# router = APIRouter()
# templates = Jinja2Templates(directory="templates")

# def get_pokemon_service(db=Depends(get_db)):
#     uow = UnitOfWork()
#     service = PokemonService(uow)
#     return service

# @router.get("/pokemon/id/{pokemon_id}", response_class=HTMLResponse)
# async def get_pokemon_by_id(
#     request: Request,
#     pokemon_id: int,
#     service: PokemonService = Depends(get_pokemon_service),
# ):
#     pokemon = await service.fetch_pokemon_by_id(pokemon_id)
#     if pokemon:
#         return templates.TemplateResponse("pokemon_detail.html", {"request": request, "pokemon": pokemon})
#     raise HTTPException(status_code=404, detail="Pokemon not found")

# @router.get("/pokemons", response_class=HTMLResponse)
# async def get_all_pokemons(
#     request: Request,
#     page: int = 1,
#     limit: int = 20,
#     name: Optional[str] = None,
#     height: Optional[int] = Query(None),
#     min_height: Optional[int] = Query(None),
#     max_height: Optional[int] = Query(None),
#     weight: Optional[int] = Query(None),
#     min_weight: Optional[int] = Query(None),
#     max_weight: Optional[int] = Query(None),
#     xp: Optional[int] = Query(None),
#     min_xp: Optional[int] = Query(None),
#     max_xp: Optional[int] = Query(None),
#     abilities: Optional[List[str]] = Query(None),
#     stats: Optional[List[str]] = Query(None),
#     types: Optional[List[str]] = Query(None),
#     base_stat: Optional[int] = Query(None),
#     min_base_stat: Optional[int] = Query(None),
#     max_base_stat: Optional[int] = Query(None),
#     is_hidden: Optional[bool] = Query(None),
#     service: PokemonService = Depends(get_pokemon_service),
# ):
#     pokemons = await service.fetch_all_pokemons(
#         page, limit, name, height, min_height, max_height, weight, min_weight, max_weight,
#         xp, min_xp, max_xp, abilities, stats, types, base_stat, min_base_stat, max_base_stat, is_hidden
#     )
    
#     return templates.TemplateResponse("pokemons.html", {"request": request, "pokemons": pokemons})