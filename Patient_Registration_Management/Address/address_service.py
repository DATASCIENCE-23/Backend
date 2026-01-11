from sqlalchemy.orm import Session
from .address_repository import AddressRepository
from .address_model import Address

class AddressService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = AddressRepository()

    def create_address(self, address_data: dict):
        address = Address(**address_data)
        return self.repository.create(self.db, address)

    def get_address(self, address_id: int):
        return self.repository.get_by_id(self.db, address_id)

    def get_addresses_by_patient(self, patient_id: int):
        return self.repository.get_by_patient_id(self.db, patient_id)

    def update_address(self, address_id: int, data: dict):
        address = self.repository.get_by_id(self.db, address_id)
        if not address:
            return None
        for key, value in data.items():
            setattr(address, key, value)
        self.db.commit()
        self.db.refresh(address)
        return address

    def delete_address(self, address_id: int):
        return self.repository.delete(self.db, address_id)
