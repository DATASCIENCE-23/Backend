from fastapi import FastAPI

# ---- Routers ----
from category.category_routes import router as category_router
from supplier.supplier_routes import router as supplier_router
from store_location.store_location_routes import router as location_router
from item.item_routes import router as item_router
from stock.stock_routes import router as stock_router
from purchase.purchase_routes import router as purchase_router
from issue.issue_routes import router as issue_router
from stock_transfer.stock_transfer_routes import router as transfer_router
from stock_adjustment.stock_adjustment_routes import router as adjustment_router
from stock_audit.stock_audit_routes import router as audit_router

app = FastAPI(
    title="Hospital Inventory Management System",
    version="1.0.0"
)

# ---- Register Routers ----
app.include_router(category_router)
app.include_router(supplier_router)
app.include_router(location_router)
app.include_router(item_router)
app.include_router(stock_router)
app.include_router(purchase_router)
app.include_router(issue_router)
app.include_router(transfer_router)
app.include_router(adjustment_router)
app.include_router(audit_router)

# ---- Root API ----
@app.get("/")
def root():
    return {"message": "Inventory Management API is running"}
