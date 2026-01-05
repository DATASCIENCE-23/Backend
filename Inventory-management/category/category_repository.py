from sqlalchemy.orm import Session
from .category_models import Category

def get_all(db: Session):
    return db.query(Category).all()

def get_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()

def create(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def delete(db: Session, category: Category):
    db.delete(category)
    db.commit()
    

def update(db: Session, category: Category, updated_data: dict):
    for key, value in updated_data.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category