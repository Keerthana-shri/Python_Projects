from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from src.schemas.pokemon_schema import PokemonInput, Ability, Stat, Type
from src.service.pokemon_service import PokemonService
from src.config.database import get_db

router = APIRouter()

def get_pokemon_service(db=Depends(get_db)):
    service = PokemonService(db)
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

@router.get("/pokemon/name/{pokemon_name}")
async def get_pokemon_by_name(
    pokemon_name: str,
    service: PokemonService = Depends(get_pokemon_service),
):
    pokemon = await service.fetch_pokemon_by_name(pokemon_name)
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

@router.get("/pokemon")
async def get_all_pokemon(
    page: int = 1,
    limit: int = 20,
    service: PokemonService = Depends(get_pokemon_service),
):
    return await service.fetch_all_pokemon(page, limit)

@router.post("/pokemon")
async def add_pokemon(
    pokemon_data: PokemonInput,
    service: PokemonService = Depends(get_pokemon_service)
):
    try:
        pokemon_data = PokemonInput(**pokemon_data.dict())
        pokemon_id = await service.create_pokemon(pokemon_data)
        # if >20:
        #     raise HTTPException(status_code=413, detail="Cannot show more than 20 pokemons at a time")
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
        raise e  # This will be caught by the custom exception handler
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

# from fastapi import APIRouter, Depends, HTTPException
# from pydantic import ValidationError
# from src.schemas.pokemon_schema import PokemonInput, Ability, Stat, Type
# from src.service.pokemon_service import PokemonService
# from src.config.database import get_db

# router = APIRouter()

# def get_pokemon_service(db=Depends(get_db)):
#     service = PokemonService(db)
#     return service

# @router.get("/pokemon/id/{pokemon_id}")
# async def get_pokemon_by_id(
#     pokemon_id: int,
#     service: PokemonService = Depends(get_pokemon_service),
# ):
#     pokemon = await service.fetch_pokemon_by_id(pokemon_id)
#     if pokemon:
#         return pokemon
#     raise HTTPException(status_code=404, detail="Pokemon not found")

# @router.get("/pokemon/name/{pokemon_name}")
# async def get_pokemon_by_name(
#     pokemon_name: str,
#     service: PokemonService = Depends(get_pokemon_service),
# ):
#     pokemon = await service.fetch_pokemon_by_name(pokemon_name)
#     if pokemon:
#         return pokemon
#     raise HTTPException(status_code=404, detail="Pokemon not found")

# @router.get("/pokemon")
# async def get_all_pokemon(
#     page: int = 1,
#     limit: int = 20,
#     service: PokemonService = Depends(get_pokemon_service),
# ):
#     return await service.fetch_all_pokemon(page, limit)

# @router.post("/pokemon")
# async def add_pokemon(
#     pokemon_data: PokemonInput,
#     service: PokemonService = Depends(get_pokemon_service)
# ):
#     errors = []

#     try:
#         pokemon_data.name = PokemonInput.validate_name(pokemon_data.name)
#     except ValidationError as e:
#         errors.append("Name must be at most 15 characters and contain only alphabets")

#     try:
#         pokemon_data.height = PokemonInput.validate_height(pokemon_data.height)
#     except ValidationError as e:
#         errors.append("Height must be at most 2000")

#     try:
#         pokemon_data.weight = PokemonInput.validate_weight(pokemon_data.weight)
#     except ValidationError as e:
#         errors.append("Weight must be at most 10000")

#     try:
#         pokemon_data.xp = PokemonInput.validate_xp(pokemon_data.xp)
#     except ValidationError as e:
#         errors.append("XP must be at most 650")

#     try:
#         pokemon_data.image_url = PokemonInput.validate_urls(pokemon_data.image_url)
#         pokemon_data.pokemon_url = PokemonInput.validate_urls(pokemon_data.pokemon_url)
#     except ValidationError as e:
#         errors.append("URL must be at most 150 characters")

#     for ability in pokemon_data.abilities:
#         try:
#             ability.name = Ability.validate_ability_name(ability.name)
#         except ValidationError as e:
#             errors.append("Ability name must be at most 15 characters and contain only alphabets")

#     for stat in pokemon_data.stats:
#         try:
#             stat.name = Stat.validate_stat_name(stat.name)
#             stat.base_stat = Stat.validate_base_stat(stat.base_stat)
#         except ValidationError as e:
#             errors.append("Stat name must contain only alphabets and base stat must be at most 300")

#     for type_ in pokemon_data.types:
#         try:
#             type_.name = Type.validate_type_name(type_.name)
#         except ValidationError as e:
#             errors.append(f"Provide the right type within ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']")

#     if errors:
#         raise HTTPException(status_code=400, detail=errors)

#     try:
#         pokemon_id = await service.create_pokemon(pokemon_data)
#         return {"details": "Pokemon added.", "id": pokemon_id}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.put("/pokemon/id/{pokemon_id}")
# async def update_pokemon_details(
#     pokemon_id: int,
#     updated_data: PokemonInput,
#     service: PokemonService = Depends(get_pokemon_service),
# ):
#     existing_pokemon = await service.fetch_pokemon_by_id(pokemon_id)
#     if not existing_pokemon:
#         raise HTTPException(status_code=404, detail="Pokemon not found")
    
#     errors = []

#     try:
#         updated_data.name = PokemonInput.validate_name(updated_data.name)
#     except ValidationError as e:
#         errors.append("Name must be at most 15 characters and contain only alphabets")

#     try:
#         updated_data.height = PokemonInput.validate_height(updated_data.height)
#     except ValidationError as e:
#         errors.append("Height must be at most 2000")

#     try:
#         updated_data.weight = PokemonInput.validate_weight(updated_data.weight)
#     except ValidationError as e:
#         errors.append("Weight must be at most 10000")

#     try:
#         updated_data.xp = PokemonInput.validate_xp(updated_data.xp)
#     except ValidationError as e:
#         errors.append("XP must be at most 650")

#     try:
#         updated_data.image_url = PokemonInput.validate_urls(updated_data.image_url)
#         updated_data.pokemon_url = PokemonInput.validate_urls(updated_data.pokemon_url)
#     except ValidationError as e:
#         errors.append("URL must be at most 150 characters")

#     for ability in updated_data.abilities:
#         try:
#             ability.name = Ability.validate_ability_name(ability.name)
#         except ValidationError as e:
#             errors.append("Ability name must be at most 15 characters and contain only alphabets")

#     for stat in updated_data.stats:
#         try:
#             stat.name = Stat.validate_stat_name(stat.name)
#             stat.base_stat = Stat.validate_base_stat(stat.base_stat)
#         except ValidationError as e:
#             errors.append("Stat name must contain only alphabets and base stat must be at most 300")

#     for type_ in updated_data.types:
#         try:
#             type_.name = Type.validate_type_name(type_.name)
#         except ValidationError as e:
#             errors.append(f"Provide the right type within ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']")

#     if errors:
#         raise HTTPException(status_code=400, detail=errors)

#     try:
#         await service.update_pokemon(pokemon_id, updated_data)
#         return {"detail": "Pokemon updated successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.delete("/pokemon/id/{pokemon_id}")
# async def remove_pokemon(
#     pokemon_id: int,
#     service: PokemonService = Depends(get_pokemon_service)
# ):
#     pokemon = await service.fetch_pokemon_by_id(pokemon_id)
#     if not pokemon:
#         raise HTTPException(status_code=404, detail="Pokemon not found")
    
#     await service.delete_pokemon(pokemon_id)
    
#     return {"detail": "Pokemon deleted"}





#-----------------------------------------------------------------------
# from fastapi import APIRouter, Depends, HTTPException
# from src.schemas.pokemon_schema import PokemonInput
# from src.service.pokemon_service import PokemonService
# from src.config.database import get_db

# router = APIRouter()

# def get_pokemon_service(db=Depends(get_db)):
#     service = PokemonService(db)
#     return service

# @router.get("/pokemon/id/{pokemon_id}")
# async def get_pokemon_by_id(
#     pokemon_id: int,
#     service: PokemonService = Depends(get_pokemon_service),
# ):
#     pokemon = await service.fetch_pokemon_by_id(pokemon_id)
#     if pokemon:
#         return pokemon
#     raise HTTPException(status_code=404, detail="Pokemon not found")

# @router.get("/pokemon/name/{pokemon_name}")
# async def get_pokemon_by_name(
#     pokemon_name: str,
#     service: PokemonService = Depends(get_pokemon_service),
# ):
#     pokemon = await service.fetch_pokemon_by_name(pokemon_name)
#     if pokemon:
#         return pokemon
#     raise HTTPException(status_code=404, detail="Pokemon not found")

# @router.get("/pokemon")
# async def get_all_pokemon(
#     page: int = 1,
#     limit: int = 20,
#     service: PokemonService = Depends(get_pokemon_service),
# ):
#     return await service.fetch_all_pokemon(page, limit)

# @router.post("/pokemon")
# async def add_pokemon(
#     pokemon_data: PokemonInput,
#     service: PokemonService = Depends(get_pokemon_service)
# ):
#     try:
#         pokemon_id = await service.create_pokemon(pokemon_data)
#         return {"details": "Pokemon added.", "id": pokemon_id}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.put("/pokemon/id/{pokemon_id}")
# async def update_pokemon_details(
#     pokemon_id: int,
#     updated_data: PokemonInput,
#     service: PokemonService = Depends(get_pokemon_service),
# ):
#     existing_pokemon = await service.fetch_pokemon_by_id(pokemon_id)
#     if not existing_pokemon:
#         raise HTTPException(status_code=404, detail="Pokemon not found")
#     try:
#         await service.update_pokemon(pokemon_id, updated_data)
#         return {"detail": "Pokemon updated successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.delete("/pokemon/id/{pokemon_id}")
# async def remove_pokemon(
#     pokemon_id: int,
#     service: PokemonService = Depends(get_pokemon_service)
# ):
#     pokemon = await service.fetch_pokemon_by_id(pokemon_id)
#     if not pokemon:
#         raise HTTPException(status_code=404, detail="Pokemon not found")
#     await service.delete_pokemon(pokemon_id)
#     return {"detail": "Pokemon deleted"}

