"""
Pharmacy Module - Pharmacist Controller
Coordinates API layer and Pharmacist Service
"""

from typing import List, Optional
from datetime import date

from sqlalchemy.orm import Session

from . import Pharmacist
from ..dispense import Dispense
from ..schemas import (
    MessageResponse,
    DispenseStatusEnum
)


from . import PharmacistService


class PharmacistController:
    """
    Thin controller around PharmacistService.
    Use this in FastAPI routes.
    """

    def __init__(self, db: Session):
        self.db = db
        self.service = PharmacistService(db)

    # ---------- Pharmacist CRUD ----------

    def create_pharmacist(self, data: dict):
        """
        data typically comes from PharmacistCreate schema:
        {
          "user_id": int,
          "first_name": str,
          "last_name": str,
          "employee_code": str,
          "license_number": str,
          "phone_number": str | None,
          "email": str | None
        }
        """
        pharmacist = self.service.create_pharmacist(data)
        return pharmacist  # let route map to schema if needed

    def get_pharmacist(self, pharmacist_id: int) -> Optional[Pharmacist]:
        return self.service.get_pharmacist(pharmacist_id)

    def get_by_user_id(self, user_id: int) -> Optional[Pharmacist]:
        return self.service.get_by_user_id(user_id)

    def list_pharmacists(
        self,
        active_only: bool = True,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Pharmacist]:
        return self.service.list_pharmacists(
            active_only=active_only,
            skip=skip,
            limit=limit,
        )

    def update_pharmacist(self, pharmacist_id: int, update_data: dict) -> Optional[Pharmacist]:
        """
        update_data typically from PharmacistUpdate schema.
        """
        return self.service.update_pharmacist(pharmacist_id, update_data)

    def deactivate_pharmacist(self, pharmacist_id: int) -> bool:
        return self.service.deactivate_pharmacist(pharmacist_id)

    # ---------- Dispense-related ----------

    def get_dispenses_by_pharmacist(
        self,
        pharmacist_id: int,
        status: Optional[DispenseStatusEnum] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Dispense]:
        return self.service.get_dispenses_by_pharmacist(
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
    ) -> dict:
        return self.service.get_dispense_stats(
            pharmacist_id=pharmacist_id,
            start_date=start_date,
            end_date=end_date,
        )
