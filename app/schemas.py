from pydantic import BaseModel, HttpUrl
from typing import List


class Ability(BaseModel):
    name: str
    is_hidden: bool


class Stat(BaseModel):
    name: str
    base_stat: int


class Type(BaseModel):
    name: str


class PokemonInput(BaseModel):
    name: str
    height: int
    weight: int
    xp: int
    image_url: HttpUrl
    pokemon_url: HttpUrl
    abilities: List[Ability]
    stats: List[Stat]
    types: List[Type]
