from repositories.insurance_repository import InsuranceRepository

class InsuranceService:
    def __init__(self):
        self.repo = InsuranceRepository()

    def get_all_insurances(self):
        insurances = self.repo.get_all()
        return [ins.to_dict() for ins in insurances]

    def get_insurance(self, insurance_id):
        insurance = self.repo.get_by_id(insurance_id)
        return insurance.to_dict() if insurance else None

    def create_insurance(self, data):
        # Basic validation
        if self.repo.get_all():
            existing = Insurance.query.filter_by(policy_number=data["policy_number"]).first()
            if existing:
                raise ValueError("Policy number already exists")

        insurance = self.repo.create(
            provider_name=data["provider_name"],
            policy_number=data["policy_number"],
            coverage_percent=data["coverage_percent"]
        )
        return insurance.to_dict()

    def update_insurance(self, insurance_id, data):
        insurance = self.repo.update(insurance_id, **data)
        return insurance.to_dict() if insurance else None

    def delete_insurance(self, insurance_id):
        return self.repo.delete(insurance_id) is not None