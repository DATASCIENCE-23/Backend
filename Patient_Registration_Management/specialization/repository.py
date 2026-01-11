from sqlalchemy.orm import Session
from .models import Specialization

class SpecializationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, specialization: Specialization):
        self.db.add(specialization)
        self.db.commit()
        self.db.refresh(specialization)
        return specialization

    def get_by_id(self, specialization_id: int):
        return self.db.query(Specialization).filter(
            Specialization.specialization_id == specialization_id
        ).first()

    def get_all(self):
        return self.db.query(Specialization).all()

    def update(self, specialization_id: int, data: dict):
        specialization = self.get_by_id(specialization_id)
        if not specialization:
            return None
        for key, value in data.items():
            setattr(specialization, key, value)
        self.db.commit()
        self.db.refresh(specialization)
        return specialization

    def delete(self, specialization_id: int):
        specialization = self.get_by_id(specialization_id)
        if specialization:
            self.db.delete(specialization)
            self.db.commit()
        return specialization
