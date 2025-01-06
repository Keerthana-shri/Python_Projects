import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from src.models.pokemon_model import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# import json
# import os
# from dotenv import load_dotenv
# from src.models.pokemon_model import (
#     Pokemon,
#     engine,
#     Base,
#     SessionLocal,
# )
# from src.schemas.pokemon_schema import (
#     PokemonInput,
#     Ability as AbilitySchema,
#     Stat as StatSchema,
#     Type as TypeSchema,
# )
# from src.repository.pokemon_repository import PokemonRepository

# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")


# async def initialize_database():
#     with open("src/data/pokedex_raw_array.json") as f:
#         pokemon_data = json.load(f)

#     db = SessionLocal()

#     Base.metadata.create_all(bind=engine)

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


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
