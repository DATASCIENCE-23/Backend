from fastapi import APIRouter
from .item_controller import (
    add_item,
    get_item_by_id,
    get_all_items,
    remove_item,
    modify_item
)

router = APIRouter(prefix="/items", tags=["Items"])

router.post("/")(add_item)
router.get("/")(get_all_items)
router.get("/{item_id}")(get_item_by_id)
router.delete("/{item_id}")(remove_item)
router.put("/{item_id}")(modify_item)
