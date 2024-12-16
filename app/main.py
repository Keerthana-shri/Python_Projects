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

"""Event triggered on application startup"""


@app.on_event("startup")
async def startup_event():
    await initialize_database()


"""Route to fetch a Pokemon by its ID"""


@app.get("/pokemon/id/{pokemon_id}")
async def get_pokemon_by_id(pokemon_id: int, db=Depends(get_db)):
    """
    Fetch a Pokemon by its unique ID.
    Args:
        pokemon_id (int): The ID of the Pokemon to fetch.
        db: The database connection dependency.
    Returns:
        dict: The Pokemon details if found.
    Raises:
        HTTPException: If the Pokemon is not found.
    """
    pokemon = await fetch_pokemon_by_id(db, pokemon_id)
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


"""Route to fetch a Pokemon by its name"""


@app.get("/pokemon/name/{pokemon_name}")
async def get_pokemon_by_name(pokemon_name: str, db=Depends(get_db)):
    """
    Fetch a Pokemon by its name.
    Args:
        pokemon_name (str): The name of the Pokemon to fetch.
        db: The database connection dependency.
    Returns:
        dict: The Pokemon details if found.
    Raises:
        HTTPException: If the Pokemon is not found.
    """
    pokemon = await fetch_pokemon_by_name(db, pokemon_name)
    if pokemon:
        return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


"""Route to fetch all Pokemon with pagination"""


@app.get("/pokemon")
async def get_all_pokemon(page: int = 1, limit: int = 20, db=Depends(get_db)):
    """
    Fetch a paginated list of all Pokemon.
    Args:
        page (int, optional): The page number to fetch. Defaults to 1.
        limit (int, optional): The number of Pokemon per page. Defaults to 20.
        db: The database connection dependency.
    Returns:
        list: A list of Pokemon details.
    """
    return await fetch_all_pokemon(db, page, limit)


"""Route to fetch hidden abilities of Pokemon"""


@app.get("/pokemon/hidden_abilities")
async def get_hidden_abilities(skip: int = 0, limit: int = 20, db=Depends(get_db)):
    """
    Fetch a list of hidden abilities of Pokemon.
    Args:
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The number of records to fetch. Defaults to 20.
        db: The database connection dependency.
    Returns:
        list: A list of hidden abilities.
    """
    return await fetch_hidden_abilities(db, skip, limit)


"""Route to add a new Pokemon to the database"""


@app.post("/pokemon")
async def add_pokemon(pokemon_data: PokemonInput, db=Depends(get_db)):
    """
    Add a new Pokemon to the database.
    Args:
        pokemon_data (PokemonInput): The data of the Pokemon to add.
        db: The database connection dependency.
    Returns:
        dict: Confirmation details with the new Pokemon ID.
    Raises:
        HTTPException: If there is an error during insertion.
    """
    try:
        pokemon_id = await create_pokemon(db, pokemon_data)
        print("main", pokemon_id)
        return {"details": "Pokemon added.", "id": pokemon_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


"""Route to update an existing Pokemon's details"""


@app.put("/pokemon/id/{pokemon_id}")
async def update_pokemon_details(
    pokemon_id: int, updated_data: PokemonInput, db=Depends(get_db)
):
    """
    Update the details of an existing Pokemon.
    Args:
        pokemon_id (int): The ID of the Pokemon to update.
        updated_data (PokemonInput): The updated Pokemon data.
        db: The database connection dependency.
    Returns:
        dict: Confirmation of the update.
    Raises:
        HTTPException: If the Pokemon is not found or there is an update error.
    """
    existing_pokemon = await fetch_pokemon_by_id(db, pokemon_id)
    if not existing_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    try:
        await update_pokemon(db, pokemon_id, updated_data)
        return {"detail": "Pokemon updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


"""Route to delete a Pokemon by its ID"""


@app.delete("/pokemon/id/{pokemon_id}")
async def remove_pokemon(pokemon_id: int, db=Depends(get_db)):
    """
    Delete a Pokemon by its unique ID.
    Args:
        pokemon_id (int): The ID of the Pokemon to delete.
        db: The database connection dependency.
    Returns:
        dict: Confirmation of the deletion.
    Raises:
        HTTPException: If the Pokemon is not found.
    """
    pokemon = await fetch_pokemon_by_id(db, pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    await delete_pokemon(db, pokemon_id)
    return {"detail": "Pokemon deleted"}
