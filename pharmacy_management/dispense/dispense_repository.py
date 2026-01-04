"""
Pharmacy Module - Dispense Repository
Handles Dispense and DispenseItem CRUD with stock management
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional, Tuple

from datetime import datetime, date, timedelta
from Electronic_Medical_Records_Management import (
    Prescription,
    PrescriptionItem,
)
from . import Dispense, DispenseItem  # adjust import path

from .. import MedicineBatchRepository  # adjust import path
from ..schemas import (
    DispenseStatusEnum,
    PrescriptionStatusEnum,)

class DispenseRepository:
    """Repository for Dispense operations"""

    @staticmethod
    def create(
        db: Session,
        dispense_data: dict,
        items_data: List[dict],
    ) -> Dispense:
        """
        Create dispense with multiple items (full/partial dispense).

        dispense_data: {
            "prescription_id": int,
            "pharmacist_id": int,
            "notes": str (optional)
        }
        items_data: [
            {
                "prescription_item_id": int,
                "batch_id": int,
                "dispensed_quantity": int,
                "unit_price": Decimal
            }
        ]
        """
        # Calculate total amount
        total = sum(
            item["dispensed_quantity"] * item["unit_price"]
            for item in items_data
        )

        dispense = Dispense(**dispense_data, total_amount=total)
        db.add(dispense)
        db.flush()  # get dispense_id

        for item_data in items_data:
            line_total = item_data["dispensed_quantity"] * item_data["unit_price"]
            item = DispenseItem(
                dispense_id=dispense.dispense_id,
                **item_data,
                line_total=line_total,
            )
            db.add(item)

            # Update batch stock
            MedicineBatchRepository.update_stock(
                db,
                item_data["batch_id"],
                -item_data["dispensed_quantity"],
            )

        # Update prescription status
        DispenseRepository._update_prescription_status(db, dispense.prescription_id)

        db.commit()
        db.refresh(dispense)
        return dispense

    @staticmethod
    def get_by_id(db: Session, dispense_id: int) -> Optional[Dispense]:
        return (
            db.query(Dispense)
            .options(joinedload(Dispense.dispense_items))
            .filter(Dispense.dispense_id == dispense_id)
            .first()
        )

    @staticmethod
    def get_by_prescription(db: Session, prescription_id: int) -> List[Dispense]:
        return (
            db.query(Dispense)
            .filter(Dispense.prescription_id == prescription_id)
            .order_by(desc(Dispense.dispensed_at))
            .all()
        )

    @staticmethod
    def update_billing_status(
        db: Session,
        dispense_id: int,
        invoice_id: int,
    ) -> Optional[Dispense]:
        """Mark dispense as billed."""
        dispense = (
            db.query(Dispense)
            .filter(Dispense.dispense_id == dispense_id)
            .first()
        )
        if dispense:
            dispense.status = DispenseStatusEnum.BILLED
            dispense.invoice_id = invoice_id
            db.commit()
            db.refresh(dispense)
        return dispense

    @staticmethod
    def get_unbilled_dispenses(db: Session) -> List[Dispense]:
        """Get completed but unbilled dispenses."""
        return (
            db.query(Dispense)
            .filter(
                Dispense.status == DispenseStatusEnum.COMPLETED,
                Dispense.invoice_id.is_(None),
            )
            .all()
        )

    @staticmethod
    def get_billing_summary(db: Session, dispense_id: int) -> Optional[dict]:
        """Get billing-friendly summary for invoice generation."""
        dispense = (
            db.query(Dispense)
            .options(
                joinedload(Dispense.dispense_items)
                .joinedload(DispenseItem.prescription_item)
                .joinedload(PrescriptionItem.medicine)
            )
            .filter(Dispense.dispense_id == dispense_id)
            .first()
        )
        if not dispense:
            return None

        items = []
        for di in dispense.dispense_items:
            med = di.prescription_item.medicine
            items.append(
                {
                    "medicine_id": med.medicine_id,
                    "medicine_name": med.medicine_name,
                    "strength": med.strength,
                    "form": med.form,
                    "dispensed_quantity": di.dispensed_quantity,
                    "unit_price": float(di.unit_price),
                    "line_total": float(di.line_total),
                }
            )

        return {
            "dispense_id": dispense.dispense_id,
            "prescription_id": dispense.prescription_id,
            "patient_id": dispense.prescription.patient_id,  # assuming prescription loaded
            "total_amount": float(dispense.total_amount),
            "items": items,
        }

    # ---------- Internal helpers ----------

    @staticmethod
    def _update_dispense_total(db: Session, dispense_id: int) -> None:
        """Recalculate dispense total after item changes."""
        dispense = db.query(Dispense).filter(Dispense.dispense_id == dispense_id).first()
        if dispense:
            dispense.total_amount = (
                db.query(func.sum(DispenseItem.line_total))
                .filter(DispenseItem.dispense_id == dispense_id)
                .scalar()
                or 0
            )
            db.flush()

    @staticmethod
    def _update_prescription_status(db: Session, prescription_id: int) -> None:
        """Update prescription status after dispense."""
        prescription = (
            db.query(Prescription)
            .options(joinedload(Prescription.prescription_items))
            .filter(Prescription.prescription_id == prescription_id)
            .first()
        )
        if not prescription:
            return

        # Total dispensed per prescription_item
        rows = (
            db.query(
                DispenseItem.prescription_item_id,
                func.sum(DispenseItem.dispensed_quantity),
            )
            .join(Dispense, Dispense.dispense_id == DispenseItem.dispense_id)
            .filter(Dispense.prescription_id == prescription_id)
            .group_by(DispenseItem.prescription_item_id)
            .all()
        )
        dispensed_map = {pid: total or 0 for pid, total in rows}

        all_full = True
        any_dispensed = False

        for item in prescription.prescription_items:
            dispensed = dispensed_map.get(item.prescription_item_id, 0)
            if dispensed > 0:
                any_dispensed = True
            if dispensed < item.prescribed_quantity:
                all_full = False

        if all_full and any_dispensed:
            prescription.status = PrescriptionStatusEnum.COMPLETED
        elif any_dispensed:
            prescription.status = PrescriptionStatusEnum.PARTIALLY_COMPLETED
        else:
            prescription.status = PrescriptionStatusEnum.PENDING

        db.flush()


class DispenseItemRepository:
    """Repository for individual DispenseItem operations"""

    @staticmethod
    def create(db: Session, dispense_item_data: dict) -> DispenseItem:
        """
        Create single dispense item (partial dispense, corrections).

        dispense_item_data: {
            "dispense_id": int,
            "prescription_item_id": int,
            "batch_id": int,
            "dispensed_quantity": int,
            "unit_price": Decimal
        }
        """
        line_total = (
            dispense_item_data["dispensed_quantity"] * dispense_item_data["unit_price"]
        )

        item = DispenseItem(**dispense_item_data, line_total=line_total)
        db.add(item)
        db.flush()

        # Update batch stock
        MedicineBatchRepository.update_stock(
            db,
            dispense_item_data["batch_id"],
            -dispense_item_data["dispensed_quantity"],
        )

        # Update parent dispense and prescription
        DispenseRepository._update_dispense_total(db, dispense_item_data["dispense_id"])
        DispenseRepository._update_prescription_status(
            db, dispense_item_data["dispense_id"]
        )

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update(
        db: Session,
        dispense_item_id: int,
        update_data: dict,
    ) -> Optional[DispenseItem]:
        """
        Update existing dispense item.

        update_data: {
            "dispensed_quantity": int (optional),
            "unit_price": Decimal (optional),
            "batch_id": int (optional)
        }
        """
        item = (
            db.query(DispenseItem)
            .filter(DispenseItem.dispense_item_id == dispense_item_id)
            .first()
        )
        if not item:
            return None

        old_quantity = item.dispensed_quantity
        old_batch_id = item.batch_id

        # Apply updates
        for key, value in update_data.items():
            if key == "dispensed_quantity":
                old_quantity = item.dispensed_quantity
                item.dispensed_quantity = value
            elif key == "unit_price":
                item.unit_price = value
            elif key == "batch_id":
                old_batch_id = item.batch_id
                item.batch_id = value

        item.line_total = item.dispensed_quantity * item.unit_price

        # Update batch stock
        if old_batch_id != item.batch_id:
            # Revert old batch
            MedicineBatchRepository.update_stock(db, old_batch_id, old_quantity)
            # Apply to new batch
            MedicineBatchRepository.update_stock(
                db, item.batch_id, -item.dispensed_quantity
            )
        elif old_quantity != item.dispensed_quantity:
            # Same batch, adjust difference
            delta = old_quantity - item.dispensed_quantity
            MedicineBatchRepository.update_stock(db, item.batch_id, delta)

        # Update parent dispense and prescription
        DispenseRepository._update_dispense_total(db, item.dispense_id)
        DispenseRepository._update_prescription_status(db, item.dispense_id)

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete(db: Session, dispense_item_id: int) -> bool:
        """Delete dispense item (returns/corrections)."""
        item = (
            db.query(DispenseItem)
            .filter(DispenseItem.dispense_item_id == dispense_item_id)
            .first()
        )
        if not item:
            return False

        dispense_id = item.dispense_id

        # Revert batch stock
        MedicineBatchRepository.update_stock(
            db, item.batch_id, item.dispensed_quantity
        )

        db.delete(item)
        db.flush()

        # Update parent dispense and prescription
        DispenseRepository._update_dispense_total(db, dispense_id)
        DispenseRepository._update_prescription_status(db, dispense_id)

        db.commit()
        return True

    @staticmethod
    def get_by_id(db: Session, dispense_item_id: int) -> Optional[DispenseItem]:
        return (
            db.query(DispenseItem)
            .filter(DispenseItem.dispense_item_id == dispense_item_id)
            .first()
        )

    @staticmethod
    def get_by_dispense(db: Session, dispense_id: int) -> List[DispenseItem]:
        return (
            db.query(DispenseItem)
            .filter(DispenseItem.dispense_id == dispense_id)
            .all()
        )
