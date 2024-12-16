async def fetch_pokemon_by_id(db, pokemon_id):
    """
    Fetchs the details of a Pokemon by its ID.
    Args:
        db: Database connection object.
        pokemon_id: Integer representing the Pokemon ID.
    Returns:
        Dictionary containing Pokemon details including abilities, stats, and types.
    """
    cursor = db.cursor()
    cursor.execute(
        """
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
    """,
        (pokemon_id,),
    )
    return cursor.fetchone()


async def fetch_pokemon_by_name(db, pokemon_name):
    """
    Fetchs the details of a Pokemon by its name.
    Args:
        db: Database connection object.
        pokemon_name: String representing the Pokémon name.
    Returns:
        Dictionary containing Pokemon details including abilities, stats, and types.
    """
    cursor = db.cursor()
    cursor.execute(
        """
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
    """,
        (pokemon_name,),
    )
    return cursor.fetchone()


async def fetch_all_pokemon(db, page, limit):
    """
    Fetchs a paginated list of all Pokemon.
    Args:
        db: Database connection object.
        page: Integer for the page number.
        limit: Integer for the number of records per page.
    Returns:
        List of dictionaries containing Pokemon details.
    """
    cursor = db.cursor()
    offset = (page - 1) * limit
    cursor.execute(
        """
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
    """,
        (offset, limit),
    )
    return cursor.fetchall()


async def fetch_hidden_abilities(db, skip, limit):
    """
    Fetchs the Pokemons with hidden abilities in a paginated manner.
    Args:
        db: Database connection object.
        skip: Integer for the number of records to skip.
        limit: Integer for the maximum number of records to return.
    Returns:
        List of Pokemon with their hidden abilities.
    """
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT pokemon.id, pokemon.name, 
            json_agg(DISTINCT jsonb_build_object('name', abilities.name, 'is_hidden', abilities.is_hidden)) AS hidden_abilities
        FROM pokemon
        JOIN abilities ON pokemon.id = abilities.pokemon_id
        WHERE abilities.is_hidden = TRUE
        GROUP BY pokemon.id
        OFFSET %s LIMIT %s;
    """,
        (skip, limit),
    )
    return cursor.fetchall()


async def create_pokemon(db, pokemon):
    """
    Inserts a new Pokemon along with its abilities, stats, and types into the database.
    Args:
        db: Database connection object.
        pokemon: Dictionary containing Pokemon data.
    Returns:
        Integer representing the ID of the newly created Pokemon.
    """
    try:
        pokemon = pokemon.model_dump(exclude_none=True)
        with db.cursor() as cursor:
            # print("Inserting Pokemon ->", pokemon.get("name"))
            cursor.execute(
                """
                INSERT INTO 
                    public.pokemon (name, height, weight, xp, image_url, pokemon_url)
                VALUES 
                    (%s, %s, %s, %s, %s, %s)
                RETURNING id
                ;
                """,
                (
                    str(pokemon.get("name")),
                    pokemon.get("height"),
                    pokemon.get("weight"),
                    pokemon.get("xp"),
                    str(pokemon.get("image_url")),
                    str(pokemon.get("pokemon_url")),
                ),
            )
            pokemon_id = cursor.fetchone()["id"]
            print("Pokemon ID ->", pokemon_id)

            for ability in pokemon.get("abilities", []):
                # print("Inserting Ability ->", ability)
                cursor.execute(
                    """
                    INSERT INTO 
                        public.abilities (pokemon_id, name, is_hidden)
                    VALUES 
                        (%s, %s, %s)
                    ;
                    """,
                    (pokemon_id, ability["name"], ability["is_hidden"]),
                )

            for stat in pokemon.get("stats", []):
                # print("Inserting Stat ->", stat)
                cursor.execute(
                    """
                    INSERT INTO 
                        public.stats (pokemon_id, name, base_stat)
                    VALUES 
                        (%s, %s, %s)
                    ;
                    """,
                    (pokemon_id, stat["name"], stat["base_stat"]),
                )

            for type_ in pokemon.get("types", []):
                # print("Inserting Type ->", type_)
                cursor.execute(
                    """
                    INSERT INTO public.types (pokemon_id, name)
                    VALUES (%s, %s)
                    ;
                    """,
                    (pokemon_id, type_["name"]),
                )

            db.commit()
            print("Insertion Successful")
            return pokemon_id

    except Exception as e:
        db.rollback()
        print("Error Occurred:", str(e))
        raise


async def update_pokemon(db, pokemon_id, updated_data):
    """
    Updates an existing Pokemon's details in the database.
    Args:
        db: Database connection object.
        pokemon_id: Integer representing the Pokemon ID.
        updated_data: Dictionary containing updated Pokemon data.
    Returns:
        Boolean indicating whether the update was successful.
    """
    try:
        updated_data = updated_data.model_dump(exclude_none=True)
        with db.cursor() as cursor:
            print("Updating Pokemon ID ->", pokemon_id)

            cursor.execute(
                """
                UPDATE public.pokemon
                SET name = %s, height = %s, weight = %s, xp = %s, image_url = %s, pokemon_url = %s
                WHERE id = %s;
                """,
                (
                    updated_data.get("name"),
                    updated_data.get("height"),
                    updated_data.get("weight"),
                    updated_data.get("xp"),
                    str(updated_data.get("image_url")),
                    str(updated_data.get("pokemon_url")),
                    pokemon_id,
                ),
            )

            cursor.execute(
                "DELETE FROM abilities WHERE pokemon_id = %s;", (pokemon_id,)
            )
            cursor.execute("DELETE FROM stats WHERE pokemon_id = %s;", (pokemon_id,))
            cursor.execute("DELETE FROM types WHERE pokemon_id = %s;", (pokemon_id,))

            for ability in updated_data.get("abilities", []):
                print("Updating Ability ->", ability)
                cursor.execute(
                    """
                    INSERT INTO public.abilities (pokemon_id, name, is_hidden)
                    VALUES (%s, %s, %s);
                    """,
                    (pokemon_id, ability["name"], ability["is_hidden"]),
                )

            for stat in updated_data.get("stats", []):
                print("Updating Stat ->", stat)
                cursor.execute(
                    """
                    INSERT INTO public.stats (pokemon_id, name, base_stat)
                    VALUES (%s, %s, %s);
                    """,
                    (pokemon_id, stat["name"], stat["base_stat"]),
                )

            for type_ in updated_data.get("types", []):
                print("Updating Type ->", type_)
                cursor.execute(
                    """
                    INSERT INTO public.types (pokemon_id, name)
                    VALUES (%s, %s);
                    """,
                    (pokemon_id, type_["name"]),
                )

            db.commit()
            print("Update Successful")
            return True

    except Exception as e:
        db.rollback()
        print("Error Occurred:", str(e))
        raise


async def delete_pokemon(db, pokemon_id):
    """
    Deletes a Pokemon and its associated data from the database.
    Args:
        db: Database connection object.
        pokemon_id: Integer representing the Pokemon ID.
    Returns:
        None
    """
    cursor = db.cursor()
    cursor.execute("DELETE FROM abilities WHERE pokemon_id = %s;", (pokemon_id,))
    cursor.execute("DELETE FROM stats WHERE pokemon_id = %s;", (pokemon_id,))
    cursor.execute("DELETE FROM types WHERE pokemon_id = %s;", (pokemon_id,))
    cursor.execute("DELETE FROM pokemon WHERE id = %s;", (pokemon_id,))
    db.commit()


