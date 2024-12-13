from fastapi import FastAPI, HTTPException, Depends
from app.database import initialize_database, get_db
from app.crud import (
    fetch_pokemon_by_id, fetch_pokemon_by_name, fetch_all_pokemon,
    fetch_hidden_abilities)

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




