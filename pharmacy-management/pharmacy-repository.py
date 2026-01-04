"""
Pharmacy Module - Repository Layer
Handles all database operations and queries
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_, desc
from typing import List, Optional, Tuple
from datetime import datetime, date, timedelta
from models import (
    Medicine, MedicineBatch, Prescription, PrescriptionItem,
    Dispense, DispenseItem, Pharmacist, PharmacyAuditLog
)
from schemas import PrescriptionStatus, DispenseStatus


class MedicineRepository:
    """Repository for Medicine CRUD operations"""

    @staticmethod
    def create(db: Session, medicine_data: dict, user_id: int) -> Medicine:
        medicine = Medicine(**medicine_data, created_by=user_id, updated_by=user_id)
        db.add(medicine)
        db.commit()
        db.refresh(medicine)
        return medicine

    @staticmethod
    def get_by_id(db: Session, medicine_id: int) -> Optional[Medicine]:
        return db.query(Medicine).filter(Medicine.medicine_id == medicine_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100,
                active_only: bool = True) -> List[Medicine]:
        query = db.query(Medicine)
        if active_only:
            query = query.filter(Medicine.is_active == True)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def search(db: Session, search_term: str, active_only: bool = True) -> List[Medicine]:
        """Search medicines by name, generic name, or code"""
        query = db.query(Medicine).filter(
            or_(
                Medicine.medicine_name.ilike(f"%{search_term}%"),
                Medicine.generic_name.ilike(f"%{search_term}%")
            )
        )
        if active_only:
            query = query.filter(Medicine.is_active == True)
        return query.all()

    @staticmethod
    def update(db: Session, medicine_id: int, update_data: dict, user_id: int) -> Optional[Medicine]:
        medicine = db.query(Medicine).filter(Medicine.medicine_id == medicine_id).first()
        if medicine:
            for key, value in update_data.items():
                if value is not None:
                    setattr(medicine, key, value)
            medicine.updated_by = user_id
            medicine.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(medicine)
        return medicine

    @staticmethod
    def check_duplicate(db: Session, name: str, strength: str, form: str,
                        exclude_id: Optional[int] = None) -> bool:
        """Check if medicine with same name, strength, and form exists"""
        query = db.query(Medicine).filter(
            Medicine.medicine_name == name,
            Medicine.strength == strength,
            Medicine.form == form
        )
        if exclude_id:
            query = query.filter(Medicine.medicine_id != exclude_id)
        return query.first() is not None

    @staticmethod
    def get_total_stock(db: Session, medicine_id: int) -> int:
        """Get total available stock across all active batches"""
        result = db.query(func.sum(MedicineBatch.quantity_in_stock)).filter(
            MedicineBatch.medicine_id == medicine_id,
            MedicineBatch.is_active == True,
            MedicineBatch.expiry_date > date.today()
        ).scalar()
        return result or 0

    @staticmethod
    def get_low_stock_medicines(db: Session) -> List[Tuple[Medicine, int]]:
        """Get medicines where stock is below reorder level"""
        medicines = db.query(Medicine).filter(Medicine.is_active == True).all()
        low_stock = []

        for med in medicines:
            total_stock = MedicineRepository.get_total_stock(db, med.medicine_id)
            if total_stock < med.reorder_level:
                low_stock.append((med, total_stock))

        return low_stock


class MedicineBatchRepository:
    """Repository for Medicine Batch operations"""

    @staticmethod
    def create(db: Session, batch_data: dict) -> MedicineBatch:
        batch = MedicineBatch(**batch_data)
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch

    @staticmethod
    def get_by_id(db: Session, batch_id: int) -> Optional[MedicineBatch]:
        return db.query(MedicineBatch).filter(MedicineBatch.batch_id == batch_id).first()

    @staticmethod
    def get_by_medicine(db: Session, medicine_id: int,
                        active_only: bool = True) -> List[MedicineBatch]:
        query = db.query(MedicineBatch).filter(MedicineBatch.medicine_id == medicine_id)
        if active_only:
            query = query.filter(
                MedicineBatch.is_active == True,
                MedicineBatch.expiry_date > date.today(),
                MedicineBatch.quantity_in_stock > 0
            )
        return query.order_by(MedicineBatch.expiry_date).all()

    @staticmethod
    def check_batch_number_exists(db: Session, batch_number: str) -> bool:
        return db.query(MedicineBatch).filter(
            MedicineBatch.batch_number == batch_number
        ).first() is not None

    @staticmethod
    def update_stock(db: Session, batch_id: int, quantity_change: int) -> Optional[MedicineBatch]:
        """Update stock quantity (can be positive for addition or negative for reduction)"""
        batch = db.query(MedicineBatch).filter(MedicineBatch.batch_id == batch_id).first()
        if batch:
            batch.quantity_in_stock += quantity_change
            if batch.quantity_in_stock < 0:
                batch.quantity_in_stock = 0
            db.commit()
            db.refresh(batch)
        return batch

    @staticmethod
    def get_nearest_expiry_batch(db: Session, medicine_id: int) -> Optional[MedicineBatch]:
        """Get batch with nearest expiry date that has stock"""
        return db.query(MedicineBatch).filter(
            MedicineBatch.medicine_id == medicine_id,
            MedicineBatch.is_active == True,
            MedicineBatch.expiry_date > date.today(),
            MedicineBatch.quantity_in_stock > 0
        ).order_by(MedicineBatch.expiry_date).first()


class PrescriptionRepository:
    """Repository for Prescription operations"""

    @staticmethod
    def create(db: Session, prescription_data: dict, items_data: List[dict]) -> Prescription:
        prescription = Prescription(**prescription_data)
        db.add(prescription)
        db.flush()

        for item_data in items_data:
            item = PrescriptionItem(prescription_id=prescription.prescription_id, **item_data)
            db.add(item)

        db.commit()
        db.refresh(prescription)
        return prescription

    @staticmethod
    def get_by_id(db: Session, prescription_id: int) -> Optional[Prescription]:
        return db.query(Prescription).options(
            joinedload(Prescription.prescription_items).joinedload(PrescriptionItem.medicine)
        ).filter(Prescription.prescription_id == prescription_id).first()

    @staticmethod
    def get_pending(db: Session, skip: int = 0, limit: int = 100) -> List[Prescription]:
        """Get all pending prescriptions"""
        return db.query(Prescription).filter(
            Prescription.status.in_([PrescriptionStatus.PENDING, PrescriptionStatus.IN_PROGRESS])
        ).order_by(desc(Prescription.created_at)).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_patient(db: Session, patient_id: int) -> List[Prescription]:
        return db.query(Prescription).filter(
            Prescription.patient_id == patient_id
        ).order_by(desc(Prescription.created_at)).all()

    @staticmethod
    def update_status(db: Session, prescription_id: int, status: PrescriptionStatus) -> Optional[Prescription]:
        prescription = db.query(Prescription).filter(
            Prescription.prescription_id == prescription_id
        ).first()
        if prescription:
            prescription.status = status
            db.commit()
            db.refresh(prescription)
        return prescription

    @staticmethod
    def check_stock_availability(db: Session, prescription_id: int) -> dict:
        """Check if all items in prescription have sufficient stock"""
        prescription = PrescriptionRepository.get_by_id(db, prescription_id)
        if not prescription:
            return {"error": "Prescription not found"}

        availability = []
        can_dispense_fully = True

        for item in prescription.prescription_items:
            total_stock = MedicineRepository.get_total_stock(db, item.medicine_id)
            can_fulfill = total_stock >= item.prescribed_quantity

            if not can_fulfill:
                can_dispense_fully = False

            availability.append({
                "medicine_id": item.medicine_id,
                "medicine_name": item.medicine.medicine_name,
                "requested_quantity": item.prescribed_quantity,
                "available_quantity": total_stock,
                "can_fulfill": can_fulfill,
                "deficit": max(0, item.prescribed_quantity - total_stock)
            })

        return {
            "prescription_id": prescription_id,
            "can_dispense_fully": can_dispense_fully,
            "items": availability
        }


class DispenseRepository:
    """Repository for Dispense operations"""

    @staticmethod
    def create(db: Session, dispense_data: dict, items_data: List[dict]) -> Dispense:
        # Calculate total amount
        total = sum(item["dispensed_quantity"] * item["unit_price"] for item in items_data)

        dispense = Dispense(**dispense_data, total_amount=total)
        db.add(dispense)
        db.flush()

        for item_data in items_data:
            line_total = item_data["dispensed_quantity"] * item_data["unit_price"]
            item = DispenseItem(
                dispense_id=dispense.dispense_id,
                **item_data,
                line_total=line_total
            )
            db.add(item)

            # Update batch stock
            MedicineBatchRepository.update_stock(
                db, item_data["batch_id"], -item_data["dispensed_quantity"]
            )

        db.commit()
        db.refresh(dispense)
        return dispense

    @staticmethod
    def get_by_id(db: Session, dispense_id: int) -> Optional[Dispense]:
        return db.query(Dispense).options(
            joinedload(Dispense.dispense_items)
        ).filter(Dispense.dispense_id == dispense_id).first()

    @staticmethod
    def get_by_prescription(db: Session, prescription_id: int) -> List[Dispense]:
        return db.query(Dispense).filter(
            Dispense.prescription_id == prescription_id
        ).order_by(desc(Dispense.dispensed_at)).all()

    @staticmethod
    def update_billing_status(db: Session, dispense_id: int, invoice_id: int) -> Optional[Dispense]:
        """Mark dispense as billed"""
        dispense = db.query(Dispense).filter(Dispense.dispense_id == dispense_id).first()
        if dispense:
            dispense.status = DispenseStatus.BILLED
            dispense.invoice_id = invoice_id
            db.commit()
            db.refresh(dispense)
        return dispense

    @staticmethod
    def get_unbilled_dispenses(db: Session) -> List[Dispense]:
        """Get all completed but not yet billed dispenses"""
        return db.query(Dispense).filter(
            Dispense.status == DispenseStatus.COMPLETED,
            Dispense.invoice_id.is_(None)
        ).all()


class PharmacyAuditRepository:
    """Repository for Audit Log operations"""

    @staticmethod
    def log_action(db: Session, user_id: int, entity_name: str, entity_id: int,
                   action_type: str, details: str, ip_address: Optional[str] = None):
        """Create an audit log entry"""
        log = PharmacyAuditLog(
            user_id=user_id,
            entity_name=entity_name,
            entity_id=entity_id,
            action_type=action_type,
            details=details,
            ip_address=ip_address
        )
        db.add(log)
        db.commit()

    @staticmethod
    def get_logs_by_entity(db: Session, entity_name: str, entity_id: int) -> List[PharmacyAuditLog]:
        """Get all audit logs for a specific entity"""
        return db.query(PharmacyAuditLog).filter(
            PharmacyAuditLog.entity_name == entity_name,
            PharmacyAuditLog.entity_id == entity_id
        ).order_by(desc(PharmacyAuditLog.action_time)).all()