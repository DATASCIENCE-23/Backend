from fastapi import APIRouter
from .store_location_controller import (
    add_location,
    get_location_by_id,
    get_all_locations,
    remove_location,
    modify_location
)

router = APIRouter(prefix="/locations", tags=["Store Location"])

router.post("/")(add_location)
router.get("/")(get_all_locations)
router.get("/{location_id}")(get_location_by_id)
router.delete("/{location_id}")(remove_location)
router.put("/{location_id}")(modify_location)