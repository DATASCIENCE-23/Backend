# items/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .repository import CategoryRepo, SupplierRepo, LocationRepo, ItemRepo
from .models import Item, StatusEnum
from .schemas import *

class MasterService:
    @staticmethod
    def create_category(db: Session, data: CategoryCreate):
        obj = Category(**data.dict())
        return CategoryRepo.create(db, obj)

    @staticmethod
    def get_category(db: Session, id: int):
        obj = CategoryRepo.get_by_id(db, id)
        if not obj:
            raise HTTPException(404, "Category not found")
        return obj

    @staticmethod
    def list_categories(db: Session):
        return CategoryRepo.get_all(db)

    @staticmethod
    def update_category(db: Session, id: int, data: CategoryUpdate):
        obj = CategoryRepo.get_by_id(db, id)
        if not obj:
            raise HTTPException(404, "Category not found")
        for k, v in data.dict(exclude_unset=True).items():
            setattr(obj, k, v)
        return CategoryRepo.update(db, obj)

    @staticmethod
    def delete_category(db: Session, id: int):
        obj = CategoryRepo.get_by_id(db, id)
        if not obj:
            raise HTTPException(404, "Category not found")
        CategoryRepo.delete(db, obj)

    # Similar methods for Supplier and StoreLocation (copy-paste and change names)

    @staticmethod
    def create_item(db: Session, data: ItemCreate):
        # Unique Item_Code
        if db.query(Item).filter(Item.code == data.code).first():
            raise HTTPException(status_code=400, detail="Item code already exists")

        # Category exists
        if not db.query(Category).filter(Category.id == data.category_id).first():
            raise HTTPException(status_code=400, detail="Category does not exist")

        obj = Item(**data.dict(), status=StatusEnum[data.status])
        return ItemRepo.create(db, obj)

    @staticmethod
    def get_item(db: Session, id: int):
        obj = ItemRepo.get_by_id(db, id)
        if not obj:
            raise HTTPException(404, "Item not found")
        return obj

    @staticmethod
    def list_items(db: Session, category_id: Optional[int] = None, status: Optional[str] = None):
        query = db.query(Item)
        if category_id:
            query = query.filter(Item.category_id == category_id)
        if status:
            query = query.filter(Item.status == status)
        return query.all()

    @staticmethod
    def update_item(db: Session, id: int, data: ItemUpdate):
        obj = ItemRepo.get_by_id(db, id)
        if not obj:
            raise HTTPException(404, "Item not found")

        update_data = data.dict(exclude_unset=True)
        if "code" in update_data and db.query(Item).filter(Item.code == update_data["code"], Item.id != id).first():
            raise HTTPException(400, "Item code already exists")

        if "category_id" in update_data and not db.query(Category).filter(Category.id == update_data["category_id"]).first():
            raise HTTPException(400, "Category does not exist")

        for k, v in update_data.items():
            if k == "status":
                setattr(obj, k, StatusEnum[v])
            else:
                setattr(obj, k, v)
        return ItemRepo.update(db, obj)

    @staticmethod
    def delete_item(db: Session, id: int):
        obj = ItemRepo.get_by_id(db, id)
        if not obj:
            raise HTTPException(404, "Item not found")
        ItemRepo.delete(db, obj)