from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List

app = FastAPI()

with open('pokedex_raw_array.json', 'r') as file:
    pokemon_data = json.load(file)

class Ability(BaseModel):
    name: str
    is_hidden: bool

class Stat(BaseModel):
    name: str
    base_stat: int

class Type(BaseModel):
    name: str

class Pokemon(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    xp: int
    image_url: str
    pokemon_url: str
    abilities: List[Ability]
    stats: List[Stat]
    types: List[Type]

@app.get('/pokemon/id/{pokemon_id}')
def get_pokemon_by_id(pokemon_id: int):
    for pokemon in pokemon_data:
        if pokemon['id'] == pokemon_id:
            return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

@app.get('/pokemon/name/{pokemon_name}')
def get_pokemon_by_name(pokemon_name: str):
    for pokemon in pokemon_data:
        if pokemon['name'].lower() == pokemon_name.lower():
            return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

@app.post('/pokemon', response_model=Pokemon)
def create_pokemon(pokemon: Pokemon):
    new_pokemon = pokemon.model_dump()
    new_pokemon["abilities"] = [ability.model_dump() for ability in pokemon.abilities]
    new_pokemon["stats"] = [stat.model_dump() for stat in pokemon.stats]
    new_pokemon["types"] = [type_.model_dump() for type_ in pokemon.types]
    pokemon_data.append(new_pokemon)
    return new_pokemon

@app.put('/pokemon/id/{pokemon_id}', response_model=Pokemon)
def update_pokemon(pokemon_id: int, updated_pokemon: Pokemon):
    for index, pokemon in enumerate(pokemon_data):
        if pokemon['id'] == pokemon_id:
            updated_data = updated_pokemon.model_dump()
            updated_data["abilities"] = [ability.model_dump() for ability in updated_pokemon.abilities]
            updated_data["stats"] = [stat.model_dump() for stat in updated_pokemon.stats]
            updated_data["types"] = [type_.model_dump() for type_ in updated_pokemon.types]
            pokemon_data[index] = updated_data
            return updated_pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

@app.delete('/pokemon/id/{pokemon_id}')
def delete_pokemon(pokemon_id: int):
    for index, pokemon in enumerate(pokemon_data):
        if pokemon['id'] == pokemon_id:
            deleted_pokemon = pokemon_data.pop(index)
            return deleted_pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")