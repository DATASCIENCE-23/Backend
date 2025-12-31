# role/routes.py
from fastapi import APIRouter
from .Role_controller import router as role_router

def register_role_routes(app):
    app.include_router(role_router, prefix="/roles", tags=["Roles"])