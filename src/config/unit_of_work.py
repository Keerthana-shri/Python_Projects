from sqlalchemy.orm import Session
from src.repository.pokemon_repository import PokemonRepository

class UnitOfWork:
    def __init__(self, db: Session):
        self.db = db
        self.pokemon_repository = PokemonRepository(db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.db.commit()
        else:
            self.db.rollback()
        self.db.close()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()