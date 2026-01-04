from address_service import AddressService


class AddressController:

    def __init__(self):
        self.service = AddressService()

    def create_address(self, db, address_data):
        return self.service.add_address(db, address_data)

    def fetch_address(self, db, address_id: int):
        return self.service.get_address(db, address_id)

    def fetch_addresses_by_patient(self, db, patient_id: int):
        return self.service.get_patient_addresses(db, patient_id)

    def delete_address(self, db, address_id: int):
        return self.service.remove_address(db, address_id)
