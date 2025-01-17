from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List

class Ability(BaseModel):
    name: str = Field(..., max_length=30)
    is_hidden: bool

    # @field_validator('name')
    # def validate_ability_name(cls, v):
    #     if len(v) > 30:
    #         raise ValueError('Ability name must be at most 30 characters')
    #     return v

class Stat(BaseModel):
    name: str = Field(..., max_length=30)
    base_stat: int

    # @field_validator('base_stat')
    # def validate_base_stat(cls, v):
    #     if v > 300:
    #         raise ValueError('Base stat must be at most 300')
    #     return v

class Type(BaseModel):
    name: str = Field(..., max_length=15)

    # @field_validator('name')
    # def validate_type_name(cls, v):
    #     if len(v) > 15:
    #         raise ValueError('Type name must be at most 15 characters')
    #     valid_types = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]
    #     if v.lower() not in valid_types:
    #         raise ValueError(f'Provide the right type within {valid_types}')
    #     return v

class PokemonInput(BaseModel):
    name: str = Field(..., max_length=30)
    height: int
    weight: int
    xp: int
    image_url: str = Field(..., max_length=300)
    pokemon_url: str = Field(..., max_length=300)
    abilities: List[Ability]
    stats: List[Stat]
    types: List[Type]

    # @field_validator('name')
    # def validate_name(cls, v):
    #     if len(v) > 30:
    #         raise ValueError('Name must be at most 30 characters')
    #     return v

    # @field_validator('height')
    # def validate_height(cls, v):
    #     if v > 2000:
    #         raise ValueError('Height must be at most 2000')
    #     return v

    # @field_validator('weight')
    # def validate_weight(cls, v):
    #     if v > 10000:
    #         raise ValueError('Weight must be at most 10000')
    #     return v

    # @field_validator('xp')
    # def validate_xp(cls, v):
    #     if v > 650:
    #         raise ValueError('XP must be at most 650')
    #     return v

    # @field_validator('image_url', 'pokemon_url')
    # def validate_urls(cls, v):
    #     url_str = str(v)
    #     if len(url_str) > 300:
    #         raise ValueError('URL must be at most 300 characters')
    #     return v
