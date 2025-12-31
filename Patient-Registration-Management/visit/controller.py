# visit/controller.py
from fastapi import APIRouter, HTTPException, Depends
from .models import Visit
from .service import VisitService
from .configuration import get_visit_service

router = APIRouter()

@router.post("/", response_model=dict)
def create_visit(
    visit: Visit,
    service: VisitService = Depends(get_visit_service)
):
    return service.create_visit(visit)

@router.get("/{visit_id}", response_model=dict)
def get_visit(
    visit_id: int,
    service: VisitService = Depends(get_visit_service)
):
    visit = service.get_visit_by_id(visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit

@router.get("/", response_model=list)
def get_all_visits(
    service: VisitService = Depends(get_visit_service)
):
    return service.get_all_visits()

@router.put("/", response_model=dict)
def update_visit(
    visit: Visit,
    service: VisitService = Depends(get_visit_service)
):
    updated = service.update_visit(visit)
    if not updated:
        raise HTTPException(status_code=404, detail="Visit not found")
    return updated

@router.delete("/{visit_id}", response_model=dict)
def delete_visit(
    visit_id: int,
    service: VisitService = Depends(get_visit_service)
):
    deleted = service.delete_visit(visit_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Visit not found")
    return {"message": "Visit deleted successfully"}
