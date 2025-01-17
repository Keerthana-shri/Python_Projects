from sqlalchemy.orm import Session
from src.models.pokemon_model import Pokemon, Ability, Stat, Type
from src.schemas.pokemon_schema import PokemonInput
from typing import List, Optional

class PokemonRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, pokemon_id: int):
        return self.db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()

    # def get_by_name(self, pokemon_name: str):
    #     return self.db.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

    # def get_all(self, offset: int, limit: int):
    #     return self.db.query(Pokemon).offset(offset).limit(limit).all()
    
    def get_all(
        self, offset: int, limit: int, name: Optional[str] = None, height: Optional[int] = None, 
        min_height: Optional[int] = None, max_height: Optional[int] = None, weight: Optional[int] = None, 
        min_weight: Optional[int] = None, max_weight: Optional[int] = None, xp: Optional[int] = None, 
        min_xp: Optional[int] = None, max_xp: Optional[int] = None, abilities: Optional[List[str]] = None, 
        stats: Optional[List[str]] = None, types: Optional[List[str]] = None, base_stat: Optional[int] = None, 
        min_base_stat: Optional[int] = None, max_base_stat: Optional[int] = None, is_hidden: Optional[bool] = None
    ):
        query = self.db.query(Pokemon)
        
        if name:
            query = query.filter(Pokemon.name == name)
        
        if height:
            query = query.filter(Pokemon.height == height)
        
        if min_height:
            query = query.filter(Pokemon.height >= min_height)
        
        if max_height:
            query = query.filter(Pokemon.height <= max_height)
        
        if weight:
            query = query.filter(Pokemon.weight == weight)
        
        if min_weight:
            query = query.filter(Pokemon.weight >= min_weight)
        
        if max_weight:
            query = query.filter(Pokemon.weight <= max_weight)
        
        if xp:
            query = query.filter(Pokemon.xp == xp)
        
        if min_xp:
            query = query.filter(Pokemon.xp >= min_xp)
        
        if max_xp:
            query = query.filter(Pokemon.xp <= max_xp)
        
        if abilities:
            query = query.join(Pokemon.abilities).filter(Ability.name.in_(abilities))
        
        if stats:
            query = query.join(Pokemon.stats).filter(Stat.name.in_(stats))
        
        if types:
            query = query.join(Pokemon.types).filter(Type.name.in_(types))
        
        if base_stat:
            query = query.join(Pokemon.stats).filter(Stat.base_stat == base_stat)
        
        if min_base_stat:
            query = query.join(Pokemon.stats).filter(Stat.base_stat >= min_base_stat)
        
        if max_base_stat:
            query = query.join(Pokemon.stats).filter(Stat.base_stat <= max_base_stat)
        
        if is_hidden is not None:
            query = query.join(Pokemon.abilities).filter(Ability.is_hidden == is_hidden)
        
        return query.offset(offset).limit(limit).all()

    def create(self, pokemon: PokemonInput):
        db_pokemon = Pokemon(
            name=pokemon.name,
            height=pokemon.height,
            weight=pokemon.weight,
            xp=pokemon.xp,
            image_url=str(pokemon.image_url),
            pokemon_url=str(pokemon.pokemon_url),
            abilities=[
                Ability(name=ability.name, is_hidden=ability.is_hidden) for ability in pokemon.abilities
            ],
            stats=[
                Stat(name=stat.name, base_stat=stat.base_stat) for stat in pokemon.stats
            ],
            types=[Type(name=type_.name) for type_ in pokemon.types],
        )
        self.db.add(db_pokemon)
        self.db.commit()
        self.db.refresh(db_pokemon)
        return db_pokemon.id

    def update(self, pokemon_id: int, updated_data: PokemonInput):
        db_pokemon = self.db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
        if not db_pokemon:
            return None
        
        db_pokemon.name = updated_data.name
        db_pokemon.height = updated_data.height
        db_pokemon.weight = updated_data.weight
        db_pokemon.xp = updated_data.xp
        db_pokemon.image_url = str(updated_data.image_url)
        db_pokemon.pokemon_url = str(updated_data.pokemon_url)

        # Clear existing relationships
        self.db.query(Ability).filter(Ability.pokemon_id == pokemon_id).delete()
        self.db.query(Stat).filter(Stat.pokemon_id == pokemon_id).delete()
        self.db.query(Type).filter(Type.pokemon_id == pokemon_id).delete()

        # Add new relationships
        db_pokemon.abilities.extend(
            [Ability(name=ability.name, is_hidden=ability.is_hidden) for ability in updated_data.abilities]
        )
        db_pokemon.stats.extend(
            [Stat(name=stat.name, base_stat=stat.base_stat) for stat in updated_data.stats]
        )
        db_pokemon.types.extend([Type(name=type_.name) for type_ in updated_data.types])

        self.db.commit()
    
    def delete(self, pokemon_id: int):
        self.db.query(Pokemon).filter(Pokemon.id == pokemon_id).delete()
        self.db.commit()

