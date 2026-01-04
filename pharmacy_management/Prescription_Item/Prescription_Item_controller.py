from fastapi import HTTPException
from .Prescription_Item_service import PrescriptionItemService

class PrescriptionItemController:

    def __init__(self, service: PrescriptionItemService):
        self.service = service

    def create(self, payload: dict):
        return self.service.create_item(payload)

    def get(self, item_id: int):
        item = self.service.get_item(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Prescription item not found")
        return item

    def get_by_prescription(self, prescription_id: int):
        return self.service.get_items_by_prescription(prescription_id)

    def update(self, item_id: int, payload: dict):
        return self.service.update_item(item_id, payload)

    def delete(self, item_id: int):
        self.service.delete_item(item_id)
        return {"message": "Prescription item deleted successfully"}
