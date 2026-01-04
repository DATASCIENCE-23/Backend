"""
Pharmacy Module - Pharmacist Service
Orchestrates pharmacist CRUD and statistics using repository
"""

from typing import List, Optional, Dict, Any
from datetime import date

from sqlalchemy.orm import Session

from .. import Pharmacist, Dispense

from . import PharmacistRepository
from .. import DispenseStatusEnum  # if you want enum on service side


class PharmacistService:
    """High-level service for pharmacist management and reporting."""

    def __init__(self, db: Session):
        self.db = db

    # ---------- Pharmacist CRUD ----------

    def create_pharmacist(self, data: Dict[str, Any]) -> Pharmacist:
        """
        data example:
        {
            "user_id": int,
            "first_name": str,
            "last_name": str,
            "employee_code": str,
            "license_number": str,
            "phone_number": str | None,
            "email": str | None,
        }
        """
        # enforce unique license and employee code
        if PharmacistRepository.check_license_exists(self.db, data["license_number"]):
            raise ValueError("License number already exists")

        if PharmacistRepository.check_employee_code_exists(
            self.db, data["employee_code"]
        ):
            raise ValueError("Employee code already exists")

        return PharmacistRepository.create(self.db, pharmacist_data=data)

    def get_pharmacist(self, pharmacist_id: int) -> Optional[Pharmacist]:
        return PharmacistRepository.get_by_id(self.db, pharmacist_id)

    def get_by_user_id(self, user_id: int) -> Optional[Pharmacist]:
        return PharmacistRepository.get_by_user_id(self.db, user_id)

    def list_pharmacists(
        self,
        active_only: bool = True,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Pharmacist]:
        return PharmacistRepository.get_all(
            self.db,
            active_only=active_only,
            skip=skip,
            limit=limit,
        )

    def update_pharmacist(
        self,
        pharmacist_id: int,
        update_data: Dict[str, Any],
    ) -> Optional[Pharmacist]:
        """
        update_data can contain any updatable fields:
        {
            "first_name": str | None,
            "last_name": str | None,
            "phone_number": str | None,
            "email": str | None,
            "employee_code": str | None,
            "license_number": str | None,
            ...
        }
        """
        # handle potential uniqueness changes
        if "license_number" in update_data and update_data["license_number"]:
            if PharmacistRepository.check_license_exists(
                self.db, update_data["license_number"]
            ):
                # also ensure it's not the same record
                existing = PharmacistRepository.get_by_id(self.db, pharmacist_id)
                if existing and existing.license_number != update_data["license_number"]:
                    raise ValueError("License number already exists")

        if "employee_code" in update_data and update_data["employee_code"]:
            if PharmacistRepository.check_employee_code_exists(
                self.db,
                update_data["employee_code"],
                exclude_id=pharmacist_id,
            ):
                raise ValueError("Employee code already exists")

        return PharmacistRepository.update(
            self.db,
            pharmacist_id=pharmacist_id,
            update_data=update_data,
        )

    def deactivate_pharmacist(self, pharmacist_id: int) -> bool:
        return PharmacistRepository.deactivate(self.db, pharmacist_id)

    # ---------- Dispense-related operations ----------

    def get_dispenses_by_pharmacist(
        self,
        pharmacist_id: int,
        status: Optional[DispenseStatusEnum] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Dispense]:
        """
        Wrapper to list dispenses done by a pharmacist.
        """
        return PharmacistRepository.get_dispenses_by_pharmacist(
            self.db,
            pharmacist_id=pharmacist_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )

    def get_dispense_stats(
        self,
        pharmacist_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Returns aggregate stats for dashboard:
        {
            "total_dispenses": int,
            "total_amount": Decimal,
            "completed_dispenses": int,
            "billed_dispenses": int
        }
        """
        return PharmacistRepository.get_dispense_stats(
            self.db,
            pharmacist_id=pharmacist_id,
            start_date=start_date,
            end_date=end_date,
        )
