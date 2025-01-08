from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, model, db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, offset: int, limit: int):
        return self.db.query(self.model).offset(offset).limit(limit).all()

    def create(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id: int, updated_data: dict):
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        for key, value in updated_data.items():
            setattr(db_obj, key, value)
        self.db.commit()
        return db_obj

    def delete(self, id: int):
        db_obj = self.get_by_id(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
        return db_obj
