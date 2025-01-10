from sqlalchemy.orm import Session
from src.config.database import SessionLocal

class UnitOfWork:
    def __init__(self):
        self.db: Session = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
        else:
            self.db.commit()
        self.db.close()