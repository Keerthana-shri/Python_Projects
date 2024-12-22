from sqlalchemy.orm import Session
from app.models import Pokemon, Ability, Stat, Type
from app.schemas import PokemonInput


async def fetch_pokemon_by_id(db: Session, pokemon_id: int):
    """
    Fetch the details of a Pokemon by its ID.
    Args:
        db (Session): The database session.
        pokemon_id (int): The ID of the Pokemon to fetch.
    Returns:
        dict: A dictionary containing the Pokemon details including abilities, stats, and types.
    """
    pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if pokemon:
        abilities = db.query(Ability).filter(Ability.pokemon_id == pokemon_id).all()
        stats = db.query(Stat).filter(Stat.pokemon_id == pokemon_id).all()
        types = db.query(Type).filter(Type.pokemon_id == pokemon_id).all()
        return {
            "id": pokemon.id,
            "name": pokemon.name,
            "height": pokemon.height,
            "weight": pokemon.weight,
            "xp": pokemon.xp,
            "image_url": pokemon.image_url,
            "pokemon_url": pokemon.pokemon_url,
            "abilities": [
                {"name": ability.name, "is_hidden": ability.is_hidden}
                for ability in abilities
            ],
            "stats": [
                {"name": stat.name, "base_stat": stat.base_stat} for stat in stats
            ],
            "types": [{"name": type_.name} for type_ in types],
        }
    return None


async def fetch_pokemon_by_name(db: Session, pokemon_name: str):
    """
    Fetch the details of a Pokemon by its name.
    Args:
        db (Session): The database session.
        pokemon_name (str): The name of the Pokemon to fetch.
    Returns:
        dict: A dictionary containing the Pokemon details including abilities, stats, and types.
    """
    pokemon = db.query(Pokemon).filter(Pokemon.name == pokemon_name).first()
    if pokemon:
        abilities = db.query(Ability).filter(Ability.pokemon_id == pokemon.id).all()
        stats = db.query(Stat).filter(Stat.pokemon_id == pokemon.id).all()
        types = db.query(Type).filter(Type.pokemon_id == pokemon.id).all()
        return {
            "id": pokemon.id,
            "name": pokemon.name,
            "height": pokemon.height,
            "weight": pokemon.weight,
            "xp": pokemon.xp,
            "image_url": pokemon.image_url,
            "pokemon_url": pokemon.pokemon_url,
            "abilities": [
                {"name": ability.name, "is_hidden": ability.is_hidden}
                for ability in abilities
            ],
            "stats": [
                {"name": stat.name, "base_stat": stat.base_stat} for stat in stats
            ],
            "types": [{"name": type_.name} for type_ in types],
        }
    return None


async def fetch_all_pokemon(db: Session, page: int, limit: int):
    """
    Fetch a paginated list of all Pokemon.
    Args:
        db (Session): The database session.
        page (int): The page number.
        limit (int): The number of records per page.
    Returns:
        list: A list of dictionaries containing Pokemon details.
    """
    offset = (page - 1) * limit
    pokemons = db.query(Pokemon).offset(offset).limit(limit).all()
    result = []
    for pokemon in pokemons:
        abilities = db.query(Ability).filter(Ability.pokemon_id == pokemon.id).all()
        stats = db.query(Stat).filter(Stat.pokemon_id == pokemon.id).all()
        types = db.query(Type).filter(Type.pokemon_id == pokemon.id).all()
        result.append(
            {
                "id": pokemon.id,
                "name": pokemon.name,
                "height": pokemon.height,
                "weight": pokemon.weight,
                "xp": pokemon.xp,
                "image_url": pokemon.image_url,
                "pokemon_url": pokemon.pokemon_url,
                "abilities": [
                    {"name": ability.name, "is_hidden": ability.is_hidden}
                    for ability in abilities
                ],
                "stats": [
                    {"name": stat.name, "base_stat": stat.base_stat} for stat in stats
                ],
                "types": [{"name": type_.name} for type_ in types],
            }
        )
    return result


async def fetch_hidden_abilities(db: Session, skip: int, limit: int):
    """
    Fetch a paginated list of Pokemon with hidden abilities.
    Args:
        db (Session): The database session.
        skip (int): The number of records to skip.
        limit (int): The number of records to return.
    Returns:
        list: A list of dictionaries containing Pokemon with hidden abilities.
    """
    pokemons = (
        db.query(Pokemon)
        .join(Ability)
        .filter(Ability.is_hidden == True)
        .offset(skip)
        .limit(limit)
        .all()
    )
    result = []
    for pokemon in pokemons:
        abilities = (
            db.query(Ability)
            .filter(Ability.pokemon_id == pokemon.id, Ability.is_hidden == True)
            .all()
        )
        result.append(
            {
                "id": pokemon.id,
                "name": pokemon.name,
                "hidden_abilities": [
                    {"name": ability.name, "is_hidden": ability.is_hidden}
                    for ability in abilities
                ],
            }
        )
    return result


async def create_pokemon(db: Session, pokemon: PokemonInput):
    """
    Create a new Pokemon in the database.
    Args:
        db (Session): The database session.
        pokemon (PokemonInput): The Pokemon data to create.
    Returns:
        int: The ID of the newly created Pokemon.
    """
    db_pokemon = Pokemon(
        name=pokemon.name,
        height=pokemon.height,
        weight=pokemon.weight,
        xp=pokemon.xp,
        image_url=str(pokemon.image_url),
        pokemon_url=str(pokemon.pokemon_url),
        abilities=[
            Ability(name=ability.name, is_hidden=ability.is_hidden)
            for ability in pokemon.abilities
        ],
        stats=[
            Stat(name=stat.name, base_stat=stat.base_stat) for stat in pokemon.stats
        ],
        types=[Type(name=type_.name) for type_ in pokemon.types],
    )
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon.id


async def update_pokemon(db: Session, pokemon_id: int, updated_data: PokemonInput):
    """
    Update an existing Pokemon in the database.
    Args:
        db (Session): The database session.
        pokemon_id (int): The ID of the Pokemon to update.
        updated_data (PokemonInput): The updated Pokemon data.
    Returns:
        None
    """
    db_pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()

    if not db_pokemon:
        return None

    db_pokemon.name = updated_data.name
    db_pokemon.height = updated_data.height
    db_pokemon.weight = updated_data.weight
    db_pokemon.xp = updated_data.xp
    db_pokemon.image_url = str(updated_data.image_url)
    db_pokemon.pokemon_url = str(updated_data.pokemon_url)

    # Clear existing relationships
    db.query(Ability).filter(Ability.pokemon_id == pokemon_id).delete()
    db.query(Stat).filter(Stat.pokemon_id == pokemon_id).delete()
    db.query(Type).filter(Type.pokemon_id == pokemon_id).delete()

    # Add new relationships
    db_pokemon.abilities.extend(
        [
            Ability(name=ability.name, is_hidden=ability.is_hidden)
            for ability in updated_data.abilities
        ]
    )
    db_pokemon.stats.extend(
        [Stat(name=stat.name, base_stat=stat.base_stat) for stat in updated_data.stats]
    )
    db_pokemon.types.extend([Type(name=type_.name) for type_ in updated_data.types])

    db.commit()


async def delete_pokemon(db: Session, pokemon_id: int):
    """
    Delete a Pokemon from the database.
    Args:
        db (Session): The database session.
        pokemon_id (int): The ID of the Pokemon to delete.
    Returns:
        None
    """
    db.query(Pokemon).filter(Pokemon.id == pokemon_id).delete()
    db.commit()
