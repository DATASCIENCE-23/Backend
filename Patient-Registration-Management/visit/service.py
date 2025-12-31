# visit/service.py
from .repository import VisitRepository
from .models import Visit

class VisitService:
    def __init__(self, repo: VisitRepository):
        self.repo = repo

    def create_visit(self, visit: Visit):
        visit.status = "ACTIVE"
        return self.repo.create_visit(visit)

    def get_visit_by_id(self, visit_id: int):
        return self.repo.get_visit_by_id(visit_id)

    def get_all_visits(self):
        return self.repo.get_all_visits()

    def update_visit(self, visit: Visit):
        existing = self.repo.get_visit_by_id(visit.visit_id)
        if not existing:
            return None
        return self.repo.update_visit(visit)

    def delete_visit(self, visit_id: int):
        return self.repo.delete_visit(visit_id)
