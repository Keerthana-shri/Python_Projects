from fastapi import FastAPI, HTTPException, Query
import json
from typing import List
from models import Pokemon, Ability, Stat, Type, HiddenAbilityPokemon

app = FastAPI()

with open('pokedex_raw_array.json', 'r') as file:
    pokemon_data = json.load(file)

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

@app.get('/pokemon/hidden_abilities', response_model=List[HiddenAbilityPokemon])
def get_pokemon_with_hidden_abilities(skip: int = 0, limit: int = 20):
    hidden_ability_pokemon = []
    for pokemon in pokemon_data:
        hidden_abilities = [ability for ability in pokemon['abilities'] if ability['is_hidden']]
        if hidden_abilities:
            hidden_ability_pokemon.append({
                "id": pokemon['id'],
                "name": pokemon['name'],
                "hidden_abilities": hidden_abilities
            })
    return hidden_ability_pokemon[skip:skip + limit]

@app.get('/pokemon', response_model=List[Pokemon])
def get_all_pokemon(skip: int = 0, limit: int = 20):
    return pokemon_data[skip:skip + limit]

@app.post('/pokemon')
def create_pokemon(pokemon: Pokemon):
    new_pokemon = pokemon.model_dump()
    new_pokemon["abilities"] = [ability.model_dump() for ability in pokemon.abilities]
    new_pokemon["stats"] = [stat.model_dump() for stat in pokemon.stats]
    new_pokemon["types"] = [pokemon_type.model_dump() for pokemon_type in pokemon.types]
    pokemon_data.append(new_pokemon)
    return {"message": f"Pokemon {pokemon.name} was created successfully"}

@app.put('/pokemon/id/{pokemon_id}')
def update_pokemon(pokemon_id: int, updated_pokemon: Pokemon):
    for index, pokemon in enumerate(pokemon_data):
        if pokemon['id'] == pokemon_id:
            updated_data = updated_pokemon.model_dump()
            updated_data["abilities"] = [ability.model_dump() for ability in updated_pokemon.abilities]
            updated_data["stats"] = [stat.model_dump() for stat in updated_pokemon.stats]
            updated_data["types"] = [pokemon_type.model_dump() for pokemon_type in updated_pokemon.types]
            pokemon_data[index] = updated_data
            return {"message": f"Pokemon {updated_pokemon.name} was updated successfully"}
    raise HTTPException(status_code=404, detail="Pokemon not found")

@app.delete('/pokemon/id/{pokemon_id}')
def delete_pokemon(pokemon_id: int):
    for index, pokemon in enumerate(pokemon_data):
        if pokemon['id'] == pokemon_id:
            deleted_pokemon = pokemon_data.pop(index)
            return {"message": f"Pokemon {deleted_pokemon['name']} was deleted successfully"}
    raise HTTPException(status_code=404, detail="Pokemon not found")