# visit/repository.py
from sqlalchemy.orm import Session
from .models import Visit

class VisitRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_visit(self, visit: Visit):
        self.db.add(visit)
        self.db.commit()
        self.db.refresh(visit)
        return visit

    def get_visit_by_id(self, visit_id: int):
        return self.db.query(Visit).filter(Visit.visit_id == visit_id).first()

    def get_all_visits(self):
        return self.db.query(Visit).all()

    def update_visit(self, visit: Visit):
        self.db.merge(visit)
        self.db.commit()
        return visit

    def delete_visit(self, visit_id: int):
        visit = self.get_visit_by_id(visit_id)
        if visit:
            self.db.delete(visit)
            self.db.commit()
        return visit
