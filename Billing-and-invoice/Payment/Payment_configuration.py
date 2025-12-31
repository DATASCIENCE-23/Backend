from fastapi import FastAPI
from database import engine
from .payment_model import Payment
from .payment_route import router as payment_router


def configure_payment_module(app: FastAPI):
    # Create tables
    Payment.metadata.create_all(bind=engine)

    # Register routes
    app.include_router(payment_router)
