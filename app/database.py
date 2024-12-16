import psycopg2
import json
import os
from psycopg2.extras import RealDictCursor
from fastapi import Depends
from dotenv import load_dotenv

"""Load environment variables from .env file"""
load_dotenv()
"""Retrieve the database URL from environment variables"""
DATABASE_URL = os.getenv("DATABASE_URL")

"""Raise an error if the DATABASE_URL is not set"""
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

"""Function to initialize the database and populate it with data if empty"""


async def initialize_database():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    """Load Pokemon data from a JSON file"""
    with open("data/pokedex_raw_array.json") as f:
        pokemon_data = json.load(f)

    """Create the 'pokemon' table if it does not exist"""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pokemon (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE,
            height INTEGER,
            weight INTEGER,
            xp INTEGER,
            image_url VARCHAR(225),
            pokemon_url VARCHAR(225)
        );
    """
    )

    """Create the 'abilities' table with a foreign key reference to pokemon"""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS abilities (
            id SERIAL PRIMARY KEY,
            pokemon_id INTEGER REFERENCES pokemon(id) ON DELETE CASCADE,
            name VARCHAR(100),
            is_hidden BOOLEAN
        );
    """
    )

    """Create the 'stats' table with a foreign key reference to pokemon"""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stats (
            id SERIAL PRIMARY KEY,
            pokemon_id INTEGER REFERENCES pokemon(id) ON DELETE CASCADE,
            name VARCHAR(100),
            base_stat INTEGER
        );
    """
    )

    """Create the 'types' table with a foreign key reference to pokemon"""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS types (
            id SERIAL PRIMARY KEY,
            pokemon_id INTEGER REFERENCES pokemon(id) ON DELETE CASCADE,
            name VARCHAR(100)

        );
    """
    )

    """Check if the 'pokemon' table is empty and populate it if necessary"""
    cursor.execute("SELECT COUNT(*) FROM pokemon;")
    if cursor.fetchone()[0] == 0:
        for pokemon in pokemon_data:
            """Insert Pokémon data into the 'pokemon' table"""
            cursor.execute(
                """
                INSERT INTO pokemon (name, height, weight, xp, image_url, pokemon_url)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """,
                (
                    pokemon["name"],
                    pokemon["height"],
                    pokemon["weight"],
                    pokemon["xp"],
                    pokemon["image_url"],
                    pokemon["pokemon_url"],
                ),
            )
            pokemon_id = cursor.fetchone()[0]

            for ability in pokemon["abilities"]:
                cursor.execute(
                    """
                    INSERT INTO abilities (pokemon_id, name, is_hidden)
                    VALUES (%s, %s, %s);
                """,
                    (pokemon_id, ability["name"], ability["is_hidden"]),
                )

            for stat in pokemon["stats"]:
                cursor.execute(
                    """
                    INSERT INTO stats (pokemon_id, name, base_stat)
                    VALUES (%s, %s, %s);
                """,
                    (pokemon_id, stat["name"], stat["base_stat"]),
                )

            for type_ in pokemon["types"]:
                cursor.execute(
                    """
                    INSERT INTO types (pokemon_id, name)
                    VALUES (%s, %s);
                """,
                    (pokemon_id, type_["name"]),
                )

    connection.commit()
    cursor.close()
    connection.close()


"""Dependency to get a database connection in FastAPI routes"""


async def get_db():
    """Establish a database connection with a RealDictCursor for dictionary-like access"""
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield connection
    finally:
        connection.close()
