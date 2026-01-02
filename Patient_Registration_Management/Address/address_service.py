from repository import AddressRepository
from model import Address

class AddressService:

    def __init__(self):
        self.repository = AddressRepository()

    def add_address(self, db, address_data):
        address = Address(**address_data)
        return self.repository.create(db, address)

    def get_address(self, db, address_id: int):
        return self.repository.get_by_id(db, address_id)

    def get_patient_addresses(self, db, patient_id: int):
        return self.repository.get_by_patient_id(db, patient_id)

    def remove_address(self, db, address_id: int):
        return self.repository.delete(db, address_id)
