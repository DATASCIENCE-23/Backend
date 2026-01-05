from sqlalchemy.orm import Session
from fastapi import HTTPException
from .category_models import Category
from . import category_repository as repository

def create_category(db: Session, data):
    # unique category name
    if repository.get_by_name(db, data.name):
        raise HTTPException(status_code=400, detail="Category already exists")

    category = Category(
        name=data.name,
        description=data.description
    )
    return repository.create(db, category)

def get_category(db: Session, category_id: int):
    category = repository.get_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def list_categories(db: Session):
    return repository.get_all(db)


from item.item_models import Item

def delete_category(db: Session, category_id: int):
    category = repository.get_by_id(db, category_id)
    if not category:
        raise HTTPException(404, "Category not found")

    # 🔴 check if category is used
    item_exists = db.query(Item).filter(
        Item.category_id == category_id
    ).first()

    if item_exists:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category. Items exist under this category."
        )

    repository.delete(db, category)
    return {"detail": "Category deleted successfully"}

    
def update_category(db: Session, category_id: int, updated_data):
    category = repository.get_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # unique category name
    if 'name' in updated_data:
        existing_category = repository.get_by_name(db, updated_data['name'])
        if existing_category and existing_category.id != category_id:
            raise HTTPException(status_code=400, detail="Category name already exists")

    return repository.update(db, category, updated_data)
