from fastapi import FastAPI, HTTPException, Query
import json
from typing import List
from models import Pokemon, Ability, Stat, Type, HiddenAbilityPokemon, PokemonUpdate

app = FastAPI()

with open("pokedex_raw_array.json", "r") as file:
    pokemon_data = json.load(file)


def find_pokemon_by_id(pokemon_id: int):
    for pokemon in pokemon_data:
        if pokemon["id"] == pokemon_id:
            return pokemon
    return None


def find_pokemon_by_name(pokemon_name: str):
    for pokemon in pokemon_data:
        if pokemon["name"].lower() == pokemon_name.lower():
            return pokemon
    return None


@app.get("/pokemon/id/{pokemon_id}")
def get_pokemon_by_id(pokemon_id: int):
    pokemon = find_pokemon_by_id(pokemon_id)
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


@app.get("/pokemon/name/{pokemon_name}")
def get_pokemon_by_name(pokemon_name: str):
    pokemon = find_pokemon_by_name(pokemon_name)
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


@app.get("/pokemon/hidden_abilities", response_model=List[HiddenAbilityPokemon])
def get_pokemon_with_hidden_abilities(skip: int = 0, limit: int = 20):
    hidden_ability_pokemon = []
    for pokemon in pokemon_data:
        hidden_abilities = [
            ability for ability in pokemon["abilities"] if ability["is_hidden"]
        ]
        if hidden_abilities:
            hidden_ability_pokemon.append(
                {
                    "id": pokemon["id"],
                    "name": pokemon["name"],
                    "hidden_abilities": hidden_abilities,
                }
            )
    return hidden_ability_pokemon[skip : skip + limit]


@app.get("/pokemon", response_model=List[Pokemon])
def get_all_pokemon(page: int = 1, limit: int = 20):
    start = (page - 1) * limit
    end = start + limit
    return pokemon_data[start:end]


@app.post("/pokemon")
def create_pokemon(pokemon: Pokemon):
    if find_pokemon_by_name(pokemon.name):
        raise HTTPException(
            status_code=400, detail="Pokemon with this name already exists"
        )

    if pokemon_data:
        max_id = 0
        for pokemon in pokemon_data:
            if pokemon["id"] > max_id:
                max_id = pokemon["id"]
        new_id = max_id + 1
    else:
        new_id = 1

    new_pokemon = pokemon.model_dump()
    new_pokemon["id"] = new_id
    new_pokemon["abilities"] = [ability.model_dump() for ability in pokemon.abilities]
    new_pokemon["stats"] = [stat.model_dump() for stat in pokemon.stats]
    new_pokemon["types"] = [pokemon_type.model_dump() for pokemon_type in pokemon.types]
    pokemon_data.append(new_pokemon)
    return {
        "message": f"Pokemon {pokemon.name} was created successfully with ID {new_id}"
    }


@app.put("/pokemon/id/{pokemon_id}")
def update_pokemon(pokemon_id: int, updated_pokemon: Pokemon):
    existing_pokemon = find_pokemon_by_id(pokemon_id)
    if not existing_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    if updated_pokemon.name != existing_pokemon["name"] and find_pokemon_by_name(
        updated_pokemon.name
    ):
        raise HTTPException(
            status_code=400, detail="Pokemon with this name already exists"
        )

    updated_data = updated_pokemon.model_dump()
    updated_data["abilities"] = [
        ability.model_dump() for ability in updated_pokemon.abilities
    ]
    updated_data["stats"] = [stat.model_dump() for stat in updated_pokemon.stats]
    updated_data["types"] = [
        pokemon_type.model_dump() for pokemon_type in updated_pokemon.types
    ]
    pokemon_data[pokemon_data.index(existing_pokemon)] = updated_data
    return {"message": f"Pokemon {updated_pokemon.name} was updated successfully"}


@app.patch("/pokemon/id/{pokemon_id}")
def patch_pokemon(pokemon_id: int, pokemon_update: PokemonUpdate):
    '''Find the existing Pokémon by ID'''
    existing_pokemon = find_pokemon_by_id(pokemon_id)
    if existing_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    '''Convert the update data to a dictionary, excluding unset fields'''
    update_data = pokemon_update.dict(exclude_unset=True)

    '''Check if the name is being updated and if it already exists'''
    if "name" in update_data:
        new_name = update_data["name"]
        if new_name != existing_pokemon["name"]:
            existing_pokemon_with_new_name = find_pokemon_by_name(new_name)
            if existing_pokemon_with_new_name is not None:
                raise HTTPException(
                    status_code=400, detail="Pokemon with this name already exists"
                )

    '''Update the existing Pokémon with the new data'''
    update_keys = list(update_data.keys())
    for key_index in range(len(update_keys)):
        key = update_keys[key_index]
        value = update_data[key]
        existing_pokemon[key] = value

    return {"message": f"Pokemon {existing_pokemon['name']} was updated successfully"}


@app.delete("/pokemon/id/{pokemon_id}")
def delete_pokemon(pokemon_id: int):
    existing_pokemon = find_pokemon_by_id(pokemon_id)
    if not existing_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    pokemon_data.remove(existing_pokemon)
    return {"message": f"Pokemon {existing_pokemon['name']} was deleted successfully"}
