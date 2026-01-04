"""
Pharmacy Module - Dispense Controller
Coordinates API layer and Dispense Service
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from . import (
    Dispense,
    DispenseItem,
)
from ..schemas import (
    DispenseCreate,
    DispenseResponse,
    DispenseItemResponse,
    DispenseBillingInfo,
)
from . import DispenseService


class DispenseController:
    """
    Thin controller around DispenseService.
    Use this in FastAPI routes.
    """

    def __init__(self, db: Session):
        self.db = db
        self.service = DispenseService(db)

    # ---------- Main dispense operations ----------

    def create_dispense(
        self,
        payload: DispenseCreate,
        pharmacist_id: int,
    ) -> DispenseResponse:
        """
        Create a new dispense (full or partial) and return response schema.
        """
        dispense: Dispense = self.service.create_dispense(
            payload=payload,
            pharmacist_id=pharmacist_id,
        )
        return self._to_dispense_response(dispense)

    def get_dispense(self, dispense_id: int) -> Optional[DispenseResponse]:
        dispense = self.service.get_dispense(dispense_id)
        if not dispense:
            return None
        return self._to_dispense_response(dispense)

    def list_dispenses_for_prescription(
        self,
        prescription_id: int,
    ) -> List[DispenseResponse]:
        dispenses = self.service.list_dispenses_for_prescription(prescription_id)
        return [self._to_dispense_response(d) for d in dispenses]

    # ---------- Billing-related ----------

    def mark_dispense_billed(
        self,
        dispense_id: int,
        invoice_id: int,
    ) -> Optional[DispenseResponse]:
        dispense = self.service.mark_dispense_billed(dispense_id, invoice_id)
        if not dispense:
            return None
        return self._to_dispense_response(dispense)

    def get_unbilled_dispenses(self) -> List[DispenseResponse]:
        dispenses = self.service.get_unbilled_dispenses()
        return [self._to_dispense_response(d) for d in dispenses]

    def get_billing_info(self, dispense_id: int) -> Optional[DispenseBillingInfo]:
        data = self.service.get_billing_info(dispense_id)
        if not data:
            return None
        # Map dict -> Pydantic schema
        return DispenseBillingInfo(
            dispense_id=data["dispense_id"],
            prescription_id=data["prescription_id"],
            patient_id=data["patient_id"],
            dispensed_at=data.get("dispensed_at"),  # or load via model
            total_amount=data["total_amount"],
            items=[
                DispenseItemResponse(**item) for item in data["items"]
            ],
            is_billed=data.get("is_billed", False),
        )

    # ---------- Dispense item operations ----------

    def add_dispense_item(self, data: dict) -> DispenseItemResponse:
        item: DispenseItem = self.service.add_dispense_item(data)
        return self._to_dispense_item_response(item)

    def update_dispense_item(
        self,
        dispense_item_id: int,
        update_data: dict,
    ) -> Optional[DispenseItemResponse]:
        item = self.service.update_dispense_item(dispense_item_id, update_data)
        if not item:
            return None
        return self._to_dispense_item_response(item)

    def delete_dispense_item(self, dispense_item_id: int) -> bool:
        return self.service.delete_dispense_item(dispense_item_id)

    def list_dispense_items(
        self,
        dispense_id: int,
    ) -> List[DispenseItemResponse]:
        items = self.service.get_dispense_items(dispense_id)
        return [self._to_dispense_item_response(i) for i in items]

    # ---------- Mapping helpers ----------

    def _to_dispense_response(self, dispense: Dispense) -> DispenseResponse:
        pharmacist_name = (
            f"{dispense.pharmacist.first_name} {dispense.pharmacist.last_name}"
            if dispense.pharmacist
            else ""
        )
        item_responses: List[DispenseItemResponse] = []
        for di in dispense.dispense_items:
            med = di.prescription_item.medicine
            item_responses.append(
                DispenseItemResponse(
                    dispense_item_id=di.dispense_item_id,
                    prescription_item_id=di.prescription_item_id,
                    medicine_name=med.medicine_name,
                    batch_number=di.batch.batch_number,
                    dispensed_quantity=di.dispensed_quantity,
                    unit_price=di.unit_price,
                    line_total=di.line_total,
                )
            )

        return DispenseResponse(
            dispense_id=dispense.dispense_id,
            prescription_id=dispense.prescription_id,
            pharmacist_id=dispense.pharmacist_id,
            pharmacist_name=pharmacist_name,
            dispensed_at=dispense.dispensed_at,
            total_amount=dispense.total_amount,
            status=dispense.status,
            notes=dispense.notes,
            items=item_responses,
        )

    def _to_dispense_item_response(
        self,
        item: DispenseItem,
    ) -> DispenseItemResponse:
        med = item.prescription_item.medicine
        return DispenseItemResponse(
            dispense_item_id=item.dispense_item_id,
            prescription_item_id=item.prescription_item_id,
            medicine_name=med.medicine_name,
            batch_number=item.batch.batch_number,
            dispensed_quantity=item.dispensed_quantity,
            unit_price=item.unit_price,
            line_total=item.line_total,
        )
