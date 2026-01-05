from sqlalchemy.orm import Session
from fastapi import HTTPException
from .item_models import Item, ItemStatus
from . import item_repository as repository
from category.category_repository import get_by_id as get_category

def create_item(db: Session, data):
    # Unique Item Code
    if repository.get_by_code(db, data.code):
        raise HTTPException(status_code=400, detail="Item code already exists")

    # Category must exist
    if not get_category(db, data.category_id):
        raise HTTPException(status_code=400, detail="Category does not exist")

    item = Item(
        code=data.code,
        name=data.name,
        unit=data.unit,
        unit_price=data.unit_price,
        minimum_stock_level=data.minimum_stock_level,
        expiry_applicable=data.expiry_applicable,
        category_id=data.category_id,
        status=ItemStatus(data.status)
    )

    return repository.create(db, item)

def get_item(db: Session, item_id: int):
    item = repository.get_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

def list_items(db: Session):
    return repository.get_all(db)

def delete_item(db: Session, item_id: int):
    item = repository.get_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    repository.delete(db, item)
    return {"detail": "Item deleted successfully"}

def update_item(db: Session, item_id: int, updated_data):
    item = repository.get_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Unique Item Code
    if 'code' in updated_data:
        existing_item = repository.get_by_code(db, updated_data['code'])
        if existing_item and existing_item.id != item_id:
            raise HTTPException(status_code=400, detail="Item code already exists")

    # If category_id is being updated, check if the new category exists
    if 'category_id' in updated_data:
        if not get_category(db, updated_data['category_id']):
            raise HTTPException(status_code=400, detail="Category does not exist")

    return repository.update(db, item, updated_data)