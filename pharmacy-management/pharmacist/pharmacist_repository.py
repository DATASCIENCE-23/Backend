"""
Pharmacy Module - Pharmacist Repository
Handles pharmacist CRUD and related queries
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from datetime import date
from typing import List, Optional

from .. import (
    Dispense, 
    Pharmacist
)
from schemas import DispenseStatus


class PharmacistRepository:
    """Repository for Pharmacist operations"""

    @staticmethod
    def create(
        db: Session,
        pharmacist_data: dict,
    ) -> Pharmacist:
        """
        Create new pharmacist.

        pharmacist_data: {
            "user_id": int,
            "first_name": str,
            "last_name": str,
            "employee_code": str,
            "license_number": str,
            "phone_number": str (optional),
            "email": str (optional)
        }
        """
        pharmacist = Pharmacist(**pharmacist_data)
        db.add(pharmacist)
        db.commit()
        db.refresh(pharmacist)
        return pharmacist

    @staticmethod
    def get_by_id(db: Session, pharmacist_id: int) -> Optional[Pharmacist]:
        """Get pharmacist by ID."""
        return (
            db.query(Pharmacist)
            .filter(Pharmacist.pharmacist_id == pharmacist_id)
            .first()
        )

    @staticmethod
    def get_by_user_id(db: Session, user_id: int) -> Optional[Pharmacist]:
        """Get pharmacist by user ID (for auth)."""
        return (
            db.query(Pharmacist)
            .filter(Pharmacist.user_id == user_id)
            .first()
        )

    @staticmethod
    def get_by_employee_code(db: Session, employee_code: str) -> Optional[Pharmacist]:
        """Get pharmacist by employee code (unique)."""
        return (
            db.query(Pharmacist)
            .filter(Pharmacist.employee_code == employee_code)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        active_only: bool = True,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Pharmacist]:
        """List all pharmacists."""
        query = db.query(Pharmacist)
        if active_only:
            query = query.filter(Pharmacist.is_active == True)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        pharmacist_id: int,
        update_data: dict,
    ) -> Optional[Pharmacist]:
        """Update pharmacist details."""
        pharmacist = (
            db.query(Pharmacist)
            .filter(Pharmacist.pharmacist_id == pharmacist_id)
            .first()
        )
        if pharmacist:
            for key, value in update_data.items():
                if value is not None:
                    setattr(pharmacist, key, value)
            db.commit()
            db.refresh(pharmacist)
        return pharmacist

    @staticmethod
    def deactivate(db: Session, pharmacist_id: int) -> bool:
        """Deactivate pharmacist (soft delete)."""
        pharmacist = (
            db.query(Pharmacist)
            .filter(Pharmacist.pharmacist_id == pharmacist_id)
            .first()
        )
        if pharmacist:
            pharmacist.is_active = False
            db.commit()
            return True
        return False

    # ---------- Dispense statistics ----------

    @staticmethod
    def get_dispenses_by_pharmacist(
        db: Session,
        pharmacist_id: int,
        status: Optional[DispenseStatus] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Dispense]:
        """Get all dispenses by this pharmacist."""
        query = (
            db.query(Dispense)
            .filter(Dispense.pharmacist_id == pharmacist_id)
            .options(joinedload(Dispense.dispense_items))
        )

        if status:
            query = query.filter(Dispense.status == status)
        if start_date:
            query = query.filter(Dispense.dispensed_at >= start_date)
        if end_date:
            query = query.filter(Dispense.dispensed_at <= end_date)

        return query.order_by(desc(Dispense.dispensed_at)).all()

    @staticmethod
    def get_dispense_stats(
        db: Session,
        pharmacist_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> dict:
        """
        Get pharmacist dispense statistics.
        Returns: {
            "total_dispenses": int,
            "total_amount": Decimal,
            "completed_dispenses": int,
            "billed_dispenses": int
        }
        """
        query = (
            db.query(
                func.count(Dispense.dispense_id).label("total_dispenses"),
                func.sum(Dispense.total_amount).label("total_amount"),
                func.count(
                    func.case(
                        [(Dispense.status == DispenseStatus.COMPLETED, 1)]
                    )
                ).label("completed_dispenses"),
                func.count(
                    func.case(
                        [(Dispense.status == DispenseStatus.BILLED, 1)]
                    )
                ).label("billed_dispenses"),
            )
            .filter(Dispense.pharmacist_id == pharmacist_id)
        )

        if start_date:
            query = query.filter(Dispense.dispensed_at >= start_date)
        if end_date:
            query = query.filter(Dispense.dispensed_at <= end_date)

        result = query.first()
        return {
            "total_dispenses": result.total_dispenses or 0,
            "total_amount": result.total_amount or 0,
            "completed_dispenses": result.completed_dispenses or 0,
            "billed_dispenses": result.billed_dispenses or 0,
        }

    @staticmethod
    def check_license_exists(db: Session, license_number: str) -> bool:
        """Check if license number already exists."""
        return (
            db.query(Pharmacist)
            .filter(Pharmacist.license_number == license_number)
            .first()
            is not None
        )

    @staticmethod
    def check_employee_code_exists(
        db: Session,
        employee_code: str,
        exclude_id: Optional[int] = None,
    ) -> bool:
        """Check if employee code already exists."""
        query = db.query(Pharmacist).filter(
            Pharmacist.employee_code == employee_code
        )
        if exclude_id:
            query = query.filter(Pharmacist.pharmacist_id != exclude_id)
        return query.first() is not None
