"""
Pharmacy Module - Medicine Service
Orchestrates medicine & batch operations using repositories
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import date

from sqlalchemy.orm import Session

from . import Medicine, MedicineBatch
from .. import (
    MedicineCreate,
    MedicineUpdate,
    MedicineResponse,
    MedicineBatchCreate,
    MedicineBatchResponse,
    LowStockMedicine,
    MedicineSearchResponse,
)
from .medicine import MedicineRepository, MedicineBatchRepository


class MedicineService:
    """High-level service for medicine catalogue and stock."""

    def __init__(self, db: Session):
        self.db = db

    # ---------- Medicine CRUD ----------

    def create_medicine(self, payload: MedicineCreate, user_id: int) -> Medicine:
        # duplicate check
        if MedicineRepository.check_duplicate(
            self.db,
            name=payload.medicine_name,
            strength=payload.strength,
            form=payload.form,
        ):
            raise ValueError("Medicine with same name, strength, and form already exists")

        medicine = MedicineRepository.create(
            self.db,
            medicine_data=payload.dict(),
            user_id=user_id,
        )
        return medicine

    def get_medicine(self, medicine_id: int) -> Optional[Medicine]:
        return MedicineRepository.get_by_id(self.db, medicine_id)

    def list_medicines(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True,
    ) -> List[Medicine]:
        return MedicineRepository.get_all(
            self.db, skip=skip, limit=limit, active_only=active_only
        )

    def search_medicines(
        self,
        term: str,
        active_only: bool = True,
    ) -> List[MedicineSearchResponse]:
        meds = MedicineRepository.search(self.db, term, active_only=active_only)
        responses: List[MedicineSearchResponse] = []

        for med in meds:
            total_stock = MedicineRepository.get_total_stock(self.db, med.medicine_id)
            nearest_batch = MedicineBatchRepository.get_nearest_expiry_batch(
                self.db, med.medicine_id
            )
            responses.append(
                MedicineSearchResponse(
                    medicine_id=med.medicine_id,
                    medicine_name=med.medicine_name,
                    generic_name=med.generic_name,
                    strength=med.strength,
                    form=med.form,
                    unit_price=med.unit_price,
                    is_active=med.is_active,
                    available_quantity=total_stock,
                    nearest_expiry=nearest_batch.expiry_date if nearest_batch else None,
                )
            )
        return responses

    def update_medicine(
        self,
        medicine_id: int,
        payload: MedicineUpdate,
        user_id: int,
    ) -> Optional[Medicine]:
        data = {k: v for k, v in payload.dict().items() if v is not None}

        # If name/strength/form are being changed, re-check duplicates
        if any(k in data for k in ("medicine_name", "strength", "form")):
            # Need current or updated values
            existing = MedicineRepository.get_by_id(self.db, medicine_id)
            if not existing:
                return None

            name = data.get("medicine_name", existing.medicine_name)
            strength = data.get("strength", existing.strength)
            form = data.get("form", existing.form)

            if MedicineRepository.check_duplicate(
                self.db,
                name=name,
                strength=strength,
                form=form,
                exclude_id=medicine_id,
            ):
                raise ValueError("Medicine with same name, strength, and form already exists")

        return MedicineRepository.update(
            self.db,
            medicine_id=medicine_id,
            update_data=data,
            user_id=user_id,
        )

    # ---------- Stock & low stock ----------

    def get_total_stock(self, medicine_id: int) -> int:
        return MedicineRepository.get_total_stock(self.db, medicine_id)

    def get_low_stock_medicines(self) -> List[LowStockMedicine]:
        rows: List[Tuple[Medicine, int]] = MedicineRepository.get_low_stock_medicines(
            self.db
        )
        result: List[LowStockMedicine] = []
        for med, total_stock in rows:
            deficit = max(0, med.reorder_level - total_stock)
            result.append(
                LowStockMedicine(
                    medicine_id=med.medicine_id,
                    medicine_name=med.medicine_name,
                    generic_name=med.generic_name,
                    strength=med.strength,
                    form=med.form,
                    available_quantity=total_stock,
                    min_quantity=med.min_quantity,
                    reorder_level=med.reorder_level,
                    deficit=deficit,
                )
            )
        return result

    # ---------- Batch operations ----------

    def create_batch(self, payload: MedicineBatchCreate) -> MedicineBatch:
        if MedicineBatchRepository.check_batch_number_exists(
            self.db, payload.batch_number
        ):
            raise ValueError("Batch number already exists")

        return MedicineBatchRepository.create(self.db, payload.dict())

    def get_batch(self, batch_id: int) -> Optional[MedicineBatch]:
        return MedicineBatchRepository.get_by_id(self.db, batch_id)

    def list_batches_for_medicine(
        self, medicine_id: int, active_only: bool = True
    ) -> List[MedicineBatch]:
        return MedicineBatchRepository.get_by_medicine(
            self.db, medicine_id, active_only=active_only
        )

    def update_batch_stock(
        self,
        batch_id: int,
        quantity_change: int,
    ) -> Optional[MedicineBatch]:
        """
        Wrapper around repository stock update.
        Positive = increase, negative = decrease.
        """
        return MedicineBatchRepository.update_stock(
            self.db, batch_id=batch_id, quantity_change=quantity_change
        )

    def get_nearest_expiry_batch(
        self,
        medicine_id: int,
    ) -> Optional[MedicineBatch]:
        return MedicineBatchRepository.get_nearest_expiry_batch(self.db, medicine_id)
