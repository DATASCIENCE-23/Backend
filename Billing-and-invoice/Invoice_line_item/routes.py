from fastapi import APIRouter
from .controller import router as line_items_router

def register_invoice_routes(app):
    app.include_router(line_items_router, prefix="/invoices")
