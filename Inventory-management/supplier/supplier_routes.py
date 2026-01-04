from fastapi import APIRouter
from .supplier_controller import (
    add_supplier,
    get_supplier_by_id,
    get_all_suppliers,
    remove_supplier
    , modify_supplier
)

router = APIRouter(prefix="/suppliers", tags=["Supplier"])

router.post("/")(add_supplier)
router.get("/")(get_all_suppliers)
router.get("/{supplier_id}")(get_supplier_by_id)
router.delete("/{supplier_id}")(remove_supplier)
router.put("/{supplier_id}")(modify_supplier)