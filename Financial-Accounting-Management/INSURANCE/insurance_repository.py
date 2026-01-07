from database import db
from models.insurance_model import Insurance

class InsuranceRepository:
    def get_all(self):
        return Insurance.query.all()

    def get_by_id(self, insurance_id):
        return Insurance.query.get(insurance_id)

    def create(self, provider_name, policy_number, coverage_percent):
        insurance = Insurance(
            provider_name=provider_name,
            policy_number=policy_number,
            coverage_percent=coverage_percent
        )
        db.session.add(insurance)
        db.session.commit()
        return insurance

    def update(self, insurance_id, **kwargs):
        insurance = self.get_by_id(insurance_id)
        if insurance:
            for key, value in kwargs.items():
                setattr(insurance, key, value)
            db.session.commit()
        return insurance

    def delete(self, insurance_id):
        insurance = self.get_by_id(insurance_id)
        if insurance:
            db.session.delete(insurance)
            db.session.commit()
        return insurance