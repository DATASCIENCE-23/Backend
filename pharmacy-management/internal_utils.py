import json


def _ensure_str_details(details: object) -> str:
    """
    Guarantee details is a JSON string.
    - If already str, return as-is.
    - If dict/list/other, json.dumps.
    """
    if isinstance(details, str):
        return details
    try:
        return json.dumps(details, default=str)
    except TypeError:
        # Fallback: string representation
        return str(details)
    
def _get_unit_price_for_batch(self, batch_id: int):
        """
        Helper to resolve unit_price for a batch.
        For now, you can:
        - Read from Medicine.unit_price, or
        - Store selling price in batch, or
        - Pass it from the controller and skip this.
        """
        batch = MedicineBatchRepository.get_by_id(self.db, batch_id)
        if not batch:
            raise ValueError(f"Batch {batch_id} not found")
        # simplest: use medicine's unit_price
        return batch.medicine.unit_price
