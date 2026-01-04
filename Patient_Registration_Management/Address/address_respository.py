from sqlalchemy.orm import Session
from model import Address

class AddressRepository:

    def create(self, db: Session, address: Address):
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    def get_by_id(self, db: Session, address_id: int):
        return db.query(Address).filter(Address.address_id == address_id).first()

    def get_by_patient_id(self, db: Session, patient_id: int):
        return db.query(Address).filter(Address.patient_id == patient_id).all()

    def delete(self, db: Session, address_id: int):
        address = self.get_by_id(db, address_id)
        if address:
            db.delete(address)
            db.commit()
        return address
