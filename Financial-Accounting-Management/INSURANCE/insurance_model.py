from database import db

class Insurance(db.Model):
    __tablename__ = "insurance"

    insurance_id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(255), nullable=False)
    policy_number = db.Column(db.String(100), unique=True, nullable=False)
    coverage_percent = db.Column(db.Float, nullable=False)  # e.g., 80.0 for 80%

    patients = db.relationship("Patient", backref="insurance", lazy=True)

    def to_dict(self):
        return {
            "insurance_id": self.insurance_id,
            "provider_name": self.provider_name,
            "policy_number": self.policy_number,
            "coverage_percent": self.coverage_percent,
        }