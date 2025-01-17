from src.repository.pokemon_repository import PokemonRepository
from src.schemas.pokemon_schema import PokemonInput
from typing import List, Optional
from src.unit_of_work import UnitOfWork

class PokemonService:
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def fetch_pokemon_by_id(self, pokemon_id: int):
        with self.uow as uow:
            repository = PokemonRepository(uow.db)
            pokemon = repository.get_by_id(pokemon_id)
            
            if pokemon:
                abilities = [ability for ability in pokemon.abilities]
                stats = [stat for stat in pokemon.stats]
                types = [type_ for type_ in pokemon.types]
                return {
                    "id": pokemon.id,
                    "name": pokemon.name,
                    "height": pokemon.height,
                    "weight": pokemon.weight,
                    "xp": pokemon.xp,
                    "image_url": pokemon.image_url,
                    "pokemon_url": pokemon.pokemon_url,
                    "abilities": [
                        {"name": ability.name, "is_hidden": ability.is_hidden} for ability in abilities
                    ],
                    "stats": [
                        {"name": stat.name, "base_stat": stat.base_stat} for stat in stats
                    ],
                    "types": [{"name": type_.name} for type_ in types],
                }
            
            return None

    async def fetch_all_pokemons(
        self, page: int, limit: int, name: Optional[str] = None, height: Optional[int] = None, 
        min_height: Optional[int] = None, max_height: Optional[int] = None, weight: Optional[int] = None, 
        min_weight: Optional[int] = None, max_weight: Optional[int] = None, xp: Optional[int] = None, 
        min_xp: Optional[int] = None, max_xp: Optional[int] = None, abilities: Optional[List[str]] = None, 
        stats: Optional[List[str]] = None, types: Optional[List[str]] = None, base_stat: Optional[int] = None, 
        min_base_stat: Optional[int] = None, max_base_stat: Optional[int] = None, is_hidden: Optional[bool] = None
    ):
        offset = (page - 1) * limit
        with self.uow as uow:
            repository = PokemonRepository(uow.db)
            pokemons = repository.get_all(
                offset, limit, name, height, min_height, max_height, weight, min_weight, 
                max_weight, xp, min_xp, max_xp, abilities, stats, types, base_stat,
                min_base_stat, max_base_stat, is_hidden
            )
            result = []
            for pokemon in pokemons:
                filtered_abilities = [
                    {"name": ability.name, "is_hidden": ability.is_hidden} 
                    for ability in pokemon.abilities 
                    if is_hidden is None or ability.is_hidden == is_hidden
                ]
                filtered_stats = [
                    {"name": stat.name, "base_stat": stat.base_stat} 
                    for stat in pokemon.stats 
                    if base_stat is None or stat.base_stat == base_stat
                ]
                types = [type_.name for type_ in pokemon.types]
                result.append(
                    {
                        "id": pokemon.id,
                        "name": pokemon.name,
                        "height": pokemon.height,
                        "weight": pokemon.weight,
                        "xp": pokemon.xp,
                        "image_url": pokemon.image_url,
                        "pokemon_url": pokemon.pokemon_url,
                        "abilities": filtered_abilities,
                        "stats": filtered_stats,
                        "types": types,
                    }
                )
            return result

    async def create_pokemon(self, pokemon_data: PokemonInput):
        with self.uow as uow:
            repository = PokemonRepository(uow.db)
            return repository.create(pokemon_data)

    async def update_pokemon(self, pokemon_id: int, updated_data: PokemonInput):
        with self.uow as uow:
            repository = PokemonRepository(uow.db)
            return repository.update(pokemon_id, updated_data)

    async def delete_pokemon(self, pokemon_id: int):
        with self.uow as uow:
            repository = PokemonRepository(uow.db)
            return repository.delete(pokemon_id)
