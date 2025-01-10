from sqlalchemy.orm import Session
from src.models.pokemon_model import Pokemon, Ability, Stat, Type
from src.schemas.pokemon_schema import PokemonInput

class PokemonRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, pokemon_id: int):
        return self.db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()

    def get_by_name(self, pokemon_name: str):
        return self.db.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

    def get_all(self, offset: int, limit: int):
        return self.db.query(Pokemon).offset(offset).limit(limit).all()

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


