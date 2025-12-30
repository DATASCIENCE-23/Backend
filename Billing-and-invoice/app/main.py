from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Health Check
# =========================
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
    }


# =========================
# Routers (later)
# =========================
# from app.routers import invoice, payment, auth
# app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
# app.include_router(invoice.router, prefix="/api/invoices", tags=["Invoices"])
# app.include_router(payment.router, prefix="/api/payments", tags=["Payments"])
