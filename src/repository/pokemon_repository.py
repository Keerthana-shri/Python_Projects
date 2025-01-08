from sqlalchemy.orm import Session
from src.models.pokemon_model import Pokemon, Ability, Stat, Type
from src.schemas.pokemon_schema import PokemonInput
from src.repository.pokemon_base_repository import BaseRepository


class PokemonRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Pokemon, db)

    def create_pokemon(self, pokemon_data: PokemonInput) -> int:
        db_pokemon = Pokemon(
            name=pokemon_data.name,
            height=pokemon_data.height,
            weight=pokemon_data.weight,
            xp=pokemon_data.xp,
            image_url=str(pokemon_data.image_url),
            pokemon_url=str(pokemon_data.pokemon_url),
            abilities=[
                Ability(name=ability.name, is_hidden=ability.is_hidden)
                for ability in pokemon_data.abilities
            ],
            stats=[
                Stat(name=stat.name, base_stat=stat.base_stat)
                for stat in pokemon_data.stats
            ],
            types=[Type(name=type_.name) for type_ in pokemon_data.types],
        )
        return super().create(db_pokemon).id

    def update_pokemon(self, pokemon_id: int, updated_data: PokemonInput) -> Pokemon:
        db_pokemon = self.get_by_id(pokemon_id)
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
            [
                Ability(name=ability.name, is_hidden=ability.is_hidden)
                for ability in updated_data.abilities
            ]
        )
        db_pokemon.stats.extend(
            [
                Stat(name=stat.name, base_stat=stat.base_stat)
                for stat in updated_data.stats
            ]
        )
        db_pokemon.types.extend([Type(name=type_.name) for type_ in updated_data.types])

        self.db.commit()
        return db_pokemon
