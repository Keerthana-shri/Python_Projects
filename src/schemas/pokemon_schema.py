from pydantic import BaseModel, field_validator, ValidationError
from typing import List

class Ability(BaseModel):
    name: str
    is_hidden: bool

    @field_validator('name')
    def validate_ability_name(cls, v):
        if len(v) > 15:
            raise ValueError('Ability name must be at most 15 characters')
        if not v.isalpha():
            raise ValueError('Ability name must contain only alphabets')
        return v

class Stat(BaseModel):
    name: str
    base_stat: int

    @field_validator('name')
    def validate_stat_name(cls, v):
        if not v.isalpha():
            raise ValueError('Stat name must contain only alphabets')
        return v

    @field_validator('base_stat')
    def validate_base_stat(cls, v):
        if v > 300:
            raise ValueError('Base stat must be at most 300')
        return v

class Type(BaseModel):
    name: str

    @field_validator('name')
    def validate_type_name(cls, v):
        if len(v) > 10:
            raise ValueError('Type name must be at most 10 characters')
        valid_types = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]
        if v.lower() not in valid_types:
            raise ValueError(f'Provide the right type within {valid_types}')
        return v

class PokemonInput(BaseModel):
    name: str
    height: int
    weight: int
    xp: int
    image_url: str
    pokemon_url: str
    abilities: List[Ability]
    stats: List[Stat]
    types: List[Type]

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) > 15:
            raise ValueError('Name must be at most 15 characters')
        if not v.isalpha():
            raise ValueError('Name must contain only alphabets')
        return v

    @field_validator('height')
    def validate_height(cls, v):
        if v > 2000:
            raise ValueError('Height must be at most 2000')
        return v

    @field_validator('weight')
    def validate_weight(cls, v):
        if v > 10000:
            raise ValueError('Weight must be at most 10000')
        return v

    @field_validator('xp')
    def validate_xp(cls, v):
        if v > 650:
            raise ValueError('XP must be at most 650')
        return v

    @field_validator('image_url', 'pokemon_url')
    def validate_urls(cls, v):
        url_str = str(v)
        if len(url_str) > 150:
            raise ValueError('URL must be at most 150 characters')
        return v

