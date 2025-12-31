# items/repository.py
from sqlalchemy.orm import Session
from .models import Category, Supplier, StoreLocation, Item

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, obj):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj):
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj):
        db.delete(obj)
        db.commit()

# Specific repos
CategoryRepo = BaseRepository(Category)
SupplierRepo = BaseRepository(Supplier)
LocationRepo = BaseRepository(StoreLocation)
ItemRepo = BaseRepository(Item)