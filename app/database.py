from sqlalchemy.orm import Session
import json
import os
from dotenv import load_dotenv
from app.models import Pokemon, Ability, Stat, Type, engine, Base, SessionLocal
from app.schemas import (
    PokemonInput,
    Ability as AbilitySchema,
    Stat as StatSchema,
    Type as TypeSchema,
)
from app.crud import create_pokemon
from fastapi import Depends

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


async def initialize_database():
    """Initialize the database and populate it with data if empty."""
    with open("data/pokedex_raw_array.json") as f:
        pokemon_data = json.load(f)

    db = SessionLocal()

    """Create tables if they don't exist"""
    Base.metadata.create_all(bind=engine)

    """Check if the 'pokemon' table is empty and populate it if necessary"""
    if not db.query(Pokemon).count():
        for pokemon in pokemon_data:
            abilities = [
                AbilitySchema(name=ability["name"], is_hidden=ability["is_hidden"])
                for ability in pokemon["abilities"]
            ]
            stats = [
                StatSchema(name=stat["name"], base_stat=stat["base_stat"])
                for stat in pokemon["stats"]
            ]
            types = [TypeSchema(name=type_["name"]) for type_ in pokemon["types"]]

            pokemon_input = PokemonInput(
                name=pokemon["name"],
                height=pokemon["height"],
                weight=pokemon["weight"],
                xp=pokemon["xp"],
                image_url=pokemon["image_url"],
                pokemon_url=pokemon["pokemon_url"],
                abilities=abilities,
                stats=stats,
                types=types,
            )

            await create_pokemon(db, pokemon_input)


def get_db():
    """This function yields a database session and ensures that the session is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
