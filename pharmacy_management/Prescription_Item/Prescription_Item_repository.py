from sqlalchemy.orm import Session
from .Prescription_Item_model import PrescriptionItem

class PrescriptionItemRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict):
        item = PrescriptionItem(**data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_by_id(self, item_id: int):
        return (
            self.db.query(PrescriptionItem)
            .filter(PrescriptionItem.prescription_item_id == item_id)
            .first()
        )


    def get_by_prescription(self, prescription_id: int):
        return self.db.query(PrescriptionItem).filter(
            PrescriptionItem.prescription_id == prescription_id
        ).all()

    def update(self, item_id: int, data: dict):
        item = self.get_by_id(item_id)
        if not item:
            raise ValueError("Prescription item not found")

        for key, value in data.items():
            if hasattr(item, key):
                setattr(item, key, value)

        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int):
        item = self.get_by_id(item_id)
        if not item:
            raise ValueError("Prescription item not found")

        self.db.delete(item)
        self.db.commit()
