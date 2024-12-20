from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Pokemon
from app.schemas import PokemonInput


async def fetch_pokemon_by_id(db: AsyncSession, pokemon_id: int):
    result = await db.execute(select(Pokemon).where(Pokemon.id == pokemon_id))
    return result.scalars().first()


async def fetch_pokemon_by_name(db: AsyncSession, pokemon_name: str):
    result = await db.execute(
        select(Pokemon).where(Pokemon.name.ilike(f"%{pokemon_name}%"))
    )
    return result.scalar()


async def fetch_all_pokemon(db: AsyncSession, page: int, limit: int):
    offset = (page - 1) * limit
    result = await db.execute(select(Pokemon).offset(offset).limit(limit))
    return result.scalars().all()


async def fetch_hidden_abilities(db: AsyncSession, skip: int, limit: int):
    result = await db.execute(select(Pokemon.abilities).offset(skip).limit(limit))
    return [row for row in result.scalars()]


async def create_pokemon(db: AsyncSession, pokemon_data: PokemonInput):
    pokemon = Pokemon(**pokemon_data.dict())
    db.add(pokemon)
    await db.commit()
    return pokemon.id


async def update_pokemon(db: AsyncSession, pokemon_id: int, updated_data: PokemonInput):
    await db.execute(
        update(Pokemon).where(Pokemon.id == pokemon_id).values(**updated_data.dict())
    )
    await db.commit()


async def delete_pokemon(db: AsyncSession, pokemon_id: int):
    await db.execute(delete(Pokemon).where(Pokemon.id == pokemon_id))
    await db.commit()
