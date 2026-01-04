from sqlalchemy.orm import Session
from .Prescription_Item_repository import PrescriptionItemRepository

class PrescriptionItemService:

    def __init__(self, db: Session):
        self.repository = PrescriptionItemRepository(db)

    def create_item(self, payload: dict):
        return self.repository.create(payload)

    def get_item(self, item_id: int):
        return self.repository.get_by_id(item_id)


    def get_items_by_prescription(self, prescription_id: int):
        return self.repository.get_by_prescription(prescription_id)

    def update_item(self, item_id: int, payload: dict):
        return self.repository.update(item_id, payload)

    def delete_item(self, item_id: int):
        self.repository.delete(item_id)
