from sqlalchemy.orm import Session
from .specialization_model import Specialization


class SpecializationRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return (
            self.db.query(Specialization)
            .filter(Specialization.is_active == True)
            .all()
        )

    def get_by_id(self, specialization_id: int):
        return (
            self.db.query(Specialization)
            .filter(
                Specialization.specialization_id == specialization_id,
                Specialization.is_active == True
            )
            .first()
        )