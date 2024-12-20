from fastapi import FastAPI, HTTPException, Depends, Body
from app.database import initialize_database, get_db
from app.crud import (
    fetch_pokemon_by_id,
    fetch_pokemon_by_name,
    fetch_all_pokemon,
    fetch_hidden_abilities,
    create_pokemon,
    delete_pokemon,
    update_pokemon,
)
from app.schemas import PokemonInput

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await initialize_database()


@app.get("/pokemon/id/{pokemon_id}")
async def get_pokemon_by_id(pokemon_id: int, db=Depends(get_db)):
    pokemon = await fetch_pokemon_by_id(db, pokemon_id)
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


@app.get("/pokemon/name/{pokemon_name}")
async def get_pokemon_by_name(pokemon_name: str, db=Depends(get_db)):
    pokemon = await fetch_pokemon_by_name(db, pokemon_name)
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


@app.get("/pokemon")
async def get_all_pokemon(page: int = 1, limit: int = 20, db=Depends(get_db)):
    return await fetch_all_pokemon(db, page, limit)


@app.get("/pokemon/hidden_abilities")
async def get_hidden_abilities(skip: int = 0, limit: int = 20, db=Depends(get_db)):
    return await fetch_hidden_abilities(db, skip, limit)


@app.post("/pokemon")
async def add_pokemon(pokemon_data: PokemonInput, db=Depends(get_db)):
    try:
        pokemon_id = await create_pokemon(db, pokemon_data)
        return {"details": "Pokemon added.", "id": pokemon_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/pokemon/id/{pokemon_id}")
async def update_pokemon_details(
    pokemon_id: int, updated_data: PokemonInput, db=Depends(get_db)
):
    existing_pokemon = await fetch_pokemon_by_id(db, pokemon_id)
    if not existing_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    try:
        await update_pokemon(db, pokemon_id, updated_data)
        return {"detail": "Pokemon updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/pokemon/id/{pokemon_id}")
async def remove_pokemon(pokemon_id: int, db=Depends(get_db)):
    pokemon = await fetch_pokemon_by_id(db, pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    await delete_pokemon(db, pokemon_id)
    return {"detail": "Pokemon deleted"}
