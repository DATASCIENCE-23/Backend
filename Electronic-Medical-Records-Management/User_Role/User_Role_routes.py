# user_role/routes.py

from fastapi import APIRouter
from .controller import router as user_role_router


def register_user_role_routes(app):
    app.include_router(
        user_role_router,
        prefix="/user-roles",
        tags=["User Roles"]
    )
