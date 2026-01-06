from fastapi import APIRouter
from Waiting_List.Waiting_List_controller import router as waiting_list_router

router = APIRouter()

router.include_router(waiting_list_router)
