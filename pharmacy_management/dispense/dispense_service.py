"""
Pharmacy Module - Dispense Service
Orchestrates dispensing logic using repositories
"""

from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session

from . import (
    Dispense,
    DispenseItem,
)
from .. import MedicineBatchRepository  # if needed
from . import DispenseRepository, DispenseItemRepository
from ..schemas import (
    DispenseCreate,
    DispenseResponse,
    DispenseItemCreate,
    DispenseBillingInfo,
)
from ..internal_utils import _get_unit_price_for_batch  


class DispenseService:
    """High-level service for dispensing and related operations."""

    def __init__(self, db: Session):
        self.db = db

    # ---------- Main dispense flows ----------

    def create_dispense(
        self,
        payload: DispenseCreate,
        pharmacist_id: int,
    ) -> Dispense:
        """
        Create a dispense from API payload.
        - Builds dispense_data and items_data dicts
        - Delegates to DispenseRepository.create()
        """
        dispense_data = {
            "prescription_id": payload.prescription_id,
            "pharmacist_id": pharmacist_id,
            "notes": payload.notes,
        }

        items_data: List[dict] = []
        for item in payload.items:
            items_data.append(
                {
                    "prescription_item_id": item.prescription_item_id,
                    "batch_id": item.batch_id,
                    "dispensed_quantity": item.dispensed_quantity,
                    # unit_price will typically come from batch/medicine
                    # but here assume you pass it from controller/route if needed
                    "unit_price": self._get_unit_price_for_batch(item.batch_id),
                }
            )

        return DispenseRepository.create(self.db, dispense_data, items_data)

    def get_dispense(self, dispense_id: int) -> Optional[Dispense]:
        """Get a dispense with its items."""
        return DispenseRepository.get_by_id(self.db, dispense_id)

    def list_dispenses_for_prescription(
        self, prescription_id: int
    ) -> List[Dispense]:
        """List all dispenses for a given prescription."""
        return DispenseRepository.get_by_prescription(self.db, prescription_id)

    # ---------- Billing / summaries ----------

    def mark_dispense_billed(
        self,
        dispense_id: int,
        invoice_id: int,
    ) -> Optional[Dispense]:
        """Mark a dispense as billed."""
        return DispenseRepository.update_billing_status(
            self.db, dispense_id, invoice_id
        )

    def get_unbilled_dispenses(self) -> List[Dispense]:
        """Get all completed but not billed dispenses."""
        return DispenseRepository.get_unbilled_dispenses(self.db)

    def get_billing_info(self, dispense_id: int) -> Optional[Dict[str, Any]]:
        """
        Return a dict suitable for billing module.
        (Controller can map it into DispenseBillingInfo schema.)
        """
        return DispenseRepository.get_billing_summary(self.db, dispense_id)

    # ---------- Dispense item operations ----------

    def add_dispense_item(self, data: Dict[str, Any]) -> DispenseItem:
        """
        Create a new dispense item for an existing dispense.
        data should contain:
          - dispense_id
          - prescription_item_id
          - batch_id
          - dispensed_quantity
          - unit_price
        """
        return DispenseItemRepository.create(self.db, data)

    def update_dispense_item(
        self,
        dispense_item_id: int,
        update_data: Dict[str, Any],
    ) -> Optional[DispenseItem]:
        return DispenseItemRepository.update(
            self.db, dispense_item_id, update_data
        )

    def delete_dispense_item(self, dispense_item_id: int) -> bool:
        return DispenseItemRepository.delete(self.db, dispense_item_id)

    def get_dispense_items(self, dispense_id: int) -> List[DispenseItem]:
        return DispenseItemRepository.get_by_dispense(self.db, dispense_id)

    

    