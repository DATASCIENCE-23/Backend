"""
Pharmacy Module - Medicine Controller
Coordinates API layer and Medicine Service
"""

from typing import List, Optional

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
from . import MedicineService


class MedicineController:
    """
    Thin controller around MedicineService.
    Use this from FastAPI routes.
    """

    def __init__(self, db: Session):
        self.db = db
        self.service = MedicineService(db)

    # ---------- Medicine operations ----------

    def create_medicine(
        self,
        payload: MedicineCreate,
        user_id: int,
    ) -> MedicineResponse:
        med: Medicine = self.service.create_medicine(payload, user_id)
        return self._to_medicine_response(med)

    def get_medicine(self, medicine_id: int) -> Optional[MedicineResponse]:
        med = self.service.get_medicine(medicine_id)
        if not med:
            return None
        # Attach total stock
        total_stock = self.service.get_total_stock(medicine_id)
        resp = self._to_medicine_response(med)
        resp.total_stock = total_stock
        return resp

    def list_medicines(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True,
    ) -> List[MedicineResponse]:
        meds = self.service.list_medicines(skip=skip, limit=limit, active_only=active_only)
        responses: List[MedicineResponse] = []
        for med in meds:
            total_stock = self.service.get_total_stock(med.medicine_id)
            resp = self._to_medicine_response(med)
            resp.total_stock = total_stock
            responses.append(resp)
        return responses

    def search_medicines(
        self,
        term: str,
        active_only: bool = True,
    ) -> List[MedicineSearchResponse]:
        return self.service.search_medicines(term, active_only=active_only)

    def update_medicine(
        self,
        medicine_id: int,
        payload: MedicineUpdate,
        user_id: int,
    ) -> Optional[MedicineResponse]:
        med = self.service.update_medicine(medicine_id, payload, user_id)
        if not med:
            return None
        resp = self._to_medicine_response(med)
        resp.total_stock = self.service.get_total_stock(medicine_id)
        return resp

    # ---------- Low stock ----------

    def get_low_stock_medicines(self) -> List[LowStockMedicine]:
        return self.service.get_low_stock_medicines()

    # ---------- Batch operations ----------

    def create_batch(self, payload: MedicineBatchCreate) -> MedicineBatchResponse:
        batch: MedicineBatch = self.service.create_batch(payload)
        return self._to_batch_response(batch)

    def get_batch(self, batch_id: int) -> Optional[MedicineBatchResponse]:
        batch = self.service.get_batch(batch_id)
        if not batch:
            return None
        return self._to_batch_response(batch)

    def list_batches_for_medicine(
        self,
        medicine_id: int,
        active_only: bool = True,
    ) -> List[MedicineBatchResponse]:
        batches = self.service.list_batches_for_medicine(medicine_id, active_only)
        return [self._to_batch_response(b) for b in batches]

    def update_batch_stock(
        self,
        batch_id: int,
        quantity_change: int,
    ) -> Optional[MedicineBatchResponse]:
        batch = self.service.update_batch_stock(batch_id, quantity_change)
        if not batch:
            return None
        return self._to_batch_response(batch)

    # ---------- Mapping helpers ----------

    def _to_medicine_response(self, med: Medicine) -> MedicineResponse:
        return MedicineResponse(
            medicine_id=med.medicine_id,
            medicine_name=med.medicine_name,
            generic_name=med.generic_name,
            strength=med.strength,
            form=med.form,
            shelf_location=med.shelf_location,
            unit_price=med.unit_price,
            is_active=med.is_active,
            min_quantity=med.min_quantity,
            reorder_level=med.reorder_level,
            created_at=med.created_at,
            updated_at=med.updated_at,
            total_stock=None,  # filled by caller when needed
        )

    def _to_batch_response(self, batch: MedicineBatch) -> MedicineBatchResponse:
        return MedicineBatchResponse(
            batch_id=batch.batch_id,
            medicine_id=batch.medicine_id,
            batch_number=batch.batch_number,
            quantity_in_stock=batch.quantity_in_stock,
            manufacture_date=batch.manufacture_date,
            expiry_date=batch.expiry_date,
            purchase_price=batch.purchase_price,
            is_active=batch.is_active,
            created_at=batch.created_at,
        )
