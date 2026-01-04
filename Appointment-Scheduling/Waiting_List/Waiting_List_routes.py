from fastapi import APIRouter
from Waiting_List.Waiting_List_controller import router as waiting_list_controller

router = APIRouter(
    prefix="/waiting-list",
    tags=["Waiting List"]
)

router.include_router(waiting_list_controller)