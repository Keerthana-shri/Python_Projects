async def fetch_pokemon_by_id(db, pokemon_id):
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.*, 
            json_agg(DISTINCT jsonb_build_object('name', a.name, 'is_hidden', a.is_hidden)) AS abilities,
            json_agg(DISTINCT jsonb_build_object('name', s.name, 'base_stat', s.base_stat)) AS stats,
            json_agg(DISTINCT jsonb_build_object('name', t.name)) AS types
        FROM pokemon p
        LEFT JOIN abilities a ON p.id = a.pokemon_id
        LEFT JOIN stats s ON p.id = s.pokemon_id
        LEFT JOIN types t ON p.id = t.pokemon_id
        WHERE p.id = %s
        GROUP BY p.id;
    """, (pokemon_id,))
    return cursor.fetchone()


async def fetch_pokemon_by_name(db, pokemon_name):
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.*, 
            json_agg(DISTINCT jsonb_build_object('name', a.name, 'is_hidden', a.is_hidden)) AS abilities,
            json_agg(DISTINCT jsonb_build_object('name', s.name, 'base_stat', s.base_stat)) AS stats,
            json_agg(DISTINCT t.name) AS types
        FROM pokemon p
        LEFT JOIN abilities a ON p.id = a.pokemon_id
        LEFT JOIN stats s ON p.id = s.pokemon_id
        LEFT JOIN types t ON p.id = t.pokemon_id
        WHERE p.name = %s
        GROUP BY p.id;
    """, (pokemon_name,))
    return cursor.fetchone()

async def fetch_all_pokemon(db, page, limit):
    cursor = db.cursor()
    offset = (page - 1) * limit
    cursor.execute("""
        SELECT p.*, 
            json_agg(DISTINCT jsonb_build_object('name', a.name, 'is_hidden', a.is_hidden)) AS abilities,
            json_agg(DISTINCT jsonb_build_object('name', s.name, 'base_stat', s.base_stat)) AS stats,
            json_agg(DISTINCT t.name) AS types
        FROM pokemon p
        LEFT JOIN abilities a ON p.id = a.pokemon_id
        LEFT JOIN stats s ON p.id = s.pokemon_id
        LEFT JOIN types t ON p.id = t.pokemon_id
        GROUP BY p.id
        OFFSET %s LIMIT %s;
    """, (offset, limit))
    return cursor.fetchall()

async def fetch_hidden_abilities(db, skip, limit):
    cursor = db.cursor()
    cursor.execute("""
        SELECT pokemon.id, pokemon.name, 
            json_agg(DISTINCT jsonb_build_object('name', abilities.name, 'is_hidden', abilities.is_hidden)) AS hidden_abilities
        FROM pokemon
        JOIN abilities ON pokemon.id = abilities.pokemon_id
        WHERE abilities.is_hidden = TRUE
        GROUP BY pokemon.id
        OFFSET %s LIMIT %s;
    """, (skip, limit))
    return cursor.fetchall()




