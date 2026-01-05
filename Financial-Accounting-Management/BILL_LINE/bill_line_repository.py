from database import db
from models.bill_line_model import BillLine

class BillLineRepository:
    def get_all(self):
        return BillLine.query.all()

    def get_by_id(self, bill_line_id):
        return BillLine.query.get(bill_line_id)

    def get_by_bill_id(self, bill_id):
        return BillLine.query.filter_by(bill_id=bill_id).all()

    def create(self, bill_id, expense_account_id, description=None, amount=None):
        line = BillLine(
            bill_id=bill_id,
            expense_account_id=expense_account_id,
            description=description,
            amount=amount
        )
        db.session.add(line)
        db.session.commit()
        return line

    def update(self, bill_line_id, **kwargs):
        line = self.get_by_id(bill_line_id)
        if line:
            for key, value in kwargs.items():
                if hasattr(line, key):
                    setattr(line, key, value)
            db.session.commit()
        return line

    def delete(self, bill_line_id):
        line = self.get_by_id(bill_line_id)
        if line:
            db.session.delete(line)
            db.session.commit()
        return line