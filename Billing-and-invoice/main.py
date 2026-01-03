from fastapi import FastAPI

# Import routers
from invoice.routes import router as invoice_router
from Invoice_line_item.controller import router as invoice_line_item_router
from Payment.Payment_route import router as payment_router
from Service_master.Service_routes import router as service_router

app = FastAPI(
    title="Billing and Invoice API",
    version="1.0.0"
)
# Register routes
app.include_router(invoice_router)
app.include_router(invoice_line_item_router, prefix="/invoices")
app.include_router(payment_router)
app.include_router(service_router)

@app.get("/")
def root():
    return {"status": "Billing and Invoice Backend running"}