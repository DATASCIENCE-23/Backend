from fastapi import APIRouter
from .category_controller import (
    add_category,
    get_category_by_id,
    get_all_categories,
    remove_category
    , modify_category
)

router = APIRouter(prefix="/categories", tags=["Category"])

router.post("/")(add_category)
router.get("/")(get_all_categories)
router.get("/{category_id}")(get_category_by_id)
router.put("/{category_id}")(modify_category)
router.delete("/{category_id}")(remove_category)
