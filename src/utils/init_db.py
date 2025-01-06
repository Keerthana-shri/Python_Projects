import json
from sqlalchemy.orm import Session
from src.models.pokemon_model import Base, Pokemon
from src.schemas.pokemon_schema import (
    PokemonInput,
    Ability as AbilitySchema,
    Stat as StatSchema,
    Type as TypeSchema,
)
from src.repository.pokemon_repository import PokemonRepository
from src.config.database import SessionLocal, engine

async def initialize_database():
    Base.metadata.create_all(bind=engine)
    await populate_database()

async def populate_database():
    with open("src/data/pokedex_raw_array.json") as f:
        pokemon_data = json.load(f)
    db: Session = SessionLocal()
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
            await PokemonRepository.create(db, pokemon_input)

# import json
# from sqlalchemy.orm import Session
# from src.models.pokemon_model import Base, Pokemon
# from src.schemas.pokemon_schema import (
#     PokemonInput,
#     Ability as AbilitySchema,
#     Stat as StatSchema,
#     Type as TypeSchema,
# )
# from src.repository.pokemon_repository import PokemonRepository
# from src.config.database import SessionLocal, engine


# async def initialize_database():
#     Base.metadata.create_all(bind=engine)
#     await populate_database()


# async def populate_database():
#     with open("src/data/pokedex_raw_array.json") as f:
#         pokemon_data = json.load(f)

#     db: Session = SessionLocal()

#     if not db.query(Pokemon).count():
#         for pokemon in pokemon_data:
#             abilities = [
#                 AbilitySchema(name=ability["name"], is_hidden=ability["is_hidden"])
#                 for ability in pokemon["abilities"]
#             ]
#             stats = [
#                 StatSchema(name=stat["name"], base_stat=stat["base_stat"])
#                 for stat in pokemon["stats"]
#             ]
#             types = [TypeSchema(name=type_["name"]) for type_ in pokemon["types"]]

#             pokemon_input = PokemonInput(
#                 name=pokemon["name"],
#                 height=pokemon["height"],
#                 weight=pokemon["weight"],
#                 xp=pokemon["xp"],
#                 image_url=pokemon["image_url"],
#                 pokemon_url=pokemon["pokemon_url"],
#                 abilities=abilities,
#                 stats=stats,
#                 types=types,
#             )

#             await PokemonRepository.create(db, pokemon_input)


