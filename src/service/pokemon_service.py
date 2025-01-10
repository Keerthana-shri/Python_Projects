from src.repository.pokemon_repository import PokemonRepository
from src.schemas.pokemon_schema import PokemonInput

class PokemonService:
    
    def __init__(self, db):
        self.repository = PokemonRepository(db)

    async def fetch_pokemon_by_id(self, pokemon_id: int):
        pokemon = self.repository.get_by_id(pokemon_id)
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

    async def fetch_pokemon_by_name(self, pokemon_name: str):
        pokemon = self.repository.get_by_name(pokemon_name)
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

    async def fetch_all_pokemon(self, page: int, limit: int):
        offset = (page - 1) * limit
        pokemons = self.repository.get_all(offset, limit)
        result = []
        for pokemon in pokemons:
            abilities = [ability for ability in pokemon.abilities]
            stats = [stat for stat in pokemon.stats]
            types = [type_ for type_ in pokemon.types]
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
                        {"name": ability.name, "is_hidden": ability.is_hidden} for ability in abilities
                    ],
                    "stats": [
                        {"name": stat.name, "base_stat": stat.base_stat} for stat in stats
                    ],
                    "types": [{"name": type_.name} for type_ in types],
                }
            )
        return result

    async def create_pokemon(self, pokemon_data: PokemonInput):
        return self.repository.create(pokemon_data)

    async def update_pokemon(self, pokemon_id: int, updated_data: PokemonInput):
        return self.repository.update(pokemon_id, updated_data)

    async def delete_pokemon(self, pokemon_id: int):
        return self.repository.delete(pokemon_id)

