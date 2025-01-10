from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Pokemon(Base):
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)  
    height = Column(Integer)
    weight = Column(Integer)
    xp = Column(Integer)
    image_url = Column(String(500)) 
    pokemon_url = Column(String(500)) 
    abilities = relationship(
        "Ability", back_populates="pokemon", cascade="all, delete-orphan"
    )
    stats = relationship("Stat", back_populates="pokemon", cascade="all, delete-orphan")
    types = relationship("Type", back_populates="pokemon", cascade="all, delete-orphan")

    hhhh = Column(String)

class Ability(Base):
    __tablename__ = "abilities"
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id", ondelete="CASCADE"))
    name = Column(String(50))  
    is_hidden = Column(Boolean)
    pokemon = relationship("Pokemon", back_populates="abilities")

class Stat(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id", ondelete="CASCADE"))
    name = Column(String)
    base_stat = Column(Integer)
    pokemon = relationship("Pokemon", back_populates="stats")

class Type(Base):
    __tablename__ = "types"
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id", ondelete="CASCADE"))
    name = Column(String(50)) 
    pokemon = relationship("Pokemon", back_populates="types")



