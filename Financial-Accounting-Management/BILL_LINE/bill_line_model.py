from database import db

class BillLine(db.Model):
    __tablename__ = "bill_line"

    bill_line_id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey("bill.bill_id"), nullable=False)
    expense_account_id = db.Column(db.Integer, nullable=False)  # References ACCOUNT table
    description = db.Column(db.String(255))
    amount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "bill_line_id": self.bill_line_id,
            "bill_id": self.bill_id,
            "expense_account_id": self.expense_account_id,
            "description": self.description,
            "amount": self.amount,
        }