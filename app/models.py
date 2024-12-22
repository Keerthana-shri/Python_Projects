from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    height = Column(Integer)
    weight = Column(Integer)
    xp = Column(Integer)
    image_url = Column(String)
    pokemon_url = Column(String)
    abilities = relationship(
        "Ability", back_populates="pokemon", cascade="all, delete-orphan"
    )
    stats = relationship("Stat", back_populates="pokemon", cascade="all, delete-orphan")
    types = relationship("Type", back_populates="pokemon", cascade="all, delete-orphan")


class Ability(Base):
    __tablename__ = "abilities"
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id", ondelete="CASCADE"))
    name = Column(String)
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
    name = Column(String)
    pokemon = relationship("Pokemon", back_populates="types")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
