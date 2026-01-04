from fastapi import APIRouter, Depends, HTTPException
from .Prescription_Item_controller import PrescriptionItemController
from .Prescription_Item_configuration import get_prescription_item_service
from .Prescription_Item_service import PrescriptionItemService

router = APIRouter(
    prefix="/prescription-items",
    tags=["EMR - Prescription Items"]
)

# Dependency
def get_controller(
    service: PrescriptionItemService = Depends(get_prescription_item_service)
):
    return PrescriptionItemController(service)


@router.post("/")
def create_prescription_item(
    payload: dict,
    controller: PrescriptionItemController = Depends(get_controller)
):
    return controller.create(payload)


@router.get("/{item_id}")
def get_prescription_item(
    item_id: int,
    controller: PrescriptionItemController = Depends(get_controller)
):
    item = controller.get(item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Prescription item not found"
        )

    return item


@router.get("/prescription/{prescription_id}")
def get_items_by_prescription(
    prescription_id: int,
    controller: PrescriptionItemController = Depends(get_controller)
):
    return controller.get_by_prescription(prescription_id)


@router.put("/{item_id}")
def update_prescription_item(
    item_id: int,
    payload: dict,
    controller: PrescriptionItemController = Depends(get_controller)
):
    return controller.update(item_id, payload)


@router.delete("/{item_id}")
def delete_prescription_item(
    item_id: int,
    controller: PrescriptionItemController = Depends(get_controller)
):
    deleted = controller.delete(item_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Prescription item not found"
        )

    return {"message": "Prescription item deleted successfully"}
