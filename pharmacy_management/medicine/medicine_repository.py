from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_, desc
from typing import List, Optional, Tuple
from datetime import datetime, date, timedelta
from . import (
    Medicine,
    MedicineBatch
)
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

