from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Patient_Registration_Management.database import get_db
from Specialization_controller import SpecializationController

router = APIRouter(
    prefix="/specializations",
    tags=["Specialization"]
)


def get_controller(db: Session = Depends(get_db)):
    return SpecializationController(db)


@router.get("/")
def list_specializations(
    controller: SpecializationController = Depends(get_controller)
):
    return controller.get_all_specializations()


@router.get("/{specialization_id}")
def get_specialization(
    specialization_id: int,
    controller: SpecializationController = Depends(get_controller)
):
    specialization = controller.get_specialization(specialization_id)
    if not specialization:
        raise HTTPException(
            status_code=404,
            detail="Specialization not found"
        )
    return specialization
