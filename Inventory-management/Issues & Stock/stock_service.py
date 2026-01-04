from sqlalchemy.orm import Session
from stock.batch_model import Batch  # Assume you have Batch model with expiry & received_date

class StockService:
    @staticmethod
    def remove(item_id: int, qty: int, store_id: int = 1, db: Session = None):
        if qty <= 0:
            return

        # FEFO (expiry first) then FIFO
        batches = db.query(Batch).filter(
            Batch.item_id == item_id,
            Batch.store_id == store_id,
            Batch.quantity > 0
        ).order_by(
            Batch.expiry_date.asc(),  # Expiring soon first
            Batch.received_date.asc()  # Then oldest
        ).all()

        remaining = qty
        for batch in batches:
            if remaining <= 0:
                break
            deduct = min(remaining, batch.quantity)
            batch.quantity -= deduct
            remaining -= deduct

        if remaining > 0:
            raise ValueError(f"Insufficient stock: {remaining} units missing")