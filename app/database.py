import psycopg2
import json
from psycopg2.extras import RealDictCursor
from fastapi import Depends

DATABASE_URL = "postgresql://postgres:Keerth123%40@localhost:5432/pokemon_db"

async def initialize_database():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    with open("data/pokedex_raw_array.json") as f:
        pokemon_data = json.load(f)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE,
            height INTEGER,
            weight INTEGER,
            xp INTEGER,
            image_url TEXT,
            pokemon_url TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS abilities (
            id SERIAL PRIMARY KEY,
            pokemon_id INTEGER REFERENCES pokemon(id),
            name TEXT,
            is_hidden BOOLEAN
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id SERIAL PRIMARY KEY,
            pokemon_id INTEGER REFERENCES pokemon(id),
            name TEXT,
            base_stat INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS types (
            id SERIAL PRIMARY KEY,
            pokemon_id INTEGER REFERENCES pokemon(id),
            name TEXT
        );
    """)

    # Populate database if empty
    cursor.execute("SELECT COUNT(*) FROM pokemon;")
    if cursor.fetchone()[0] == 0:
        for pokemon in pokemon_data:
            cursor.execute("""
                INSERT INTO pokemon (name, height, weight, xp, image_url, pokemon_url)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (pokemon['name'], pokemon['height'], pokemon['weight'], pokemon['xp'], pokemon['image_url'], pokemon['pokemon_url']))
            pokemon_id = cursor.fetchone()[0]

            for ability in pokemon['abilities']:
                cursor.execute("""
                    INSERT INTO abilities (pokemon_id, name, is_hidden)
                    VALUES (%s, %s, %s);
                """, (pokemon_id, ability['name'], ability['is_hidden']))

            for stat in pokemon['stats']:
                cursor.execute("""
                    INSERT INTO stats (pokemon_id, name, base_stat)
                    VALUES (%s, %s, %s);
                """, (pokemon_id, stat.get('name'), stat.get('base_stat')))

            for type_ in pokemon['types']:
                cursor.execute("""
                    INSERT INTO types (pokemon_id, name)
                    VALUES (%s, %s);
                """, (pokemon_id, type_.get('name')))


    connection.commit()
    cursor.close()
    connection.close()

async def get_db():
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield connection
    finally:
        connection.close()

