from fastapi import FastAPI

# Import routers
from User.User_routes import router as user_router
from Role.Role_routes import router as role_router
from User_Role.User_Role_routes import router as user_role_router
from Doctor.Doctor_routes import router as doctor_router
from Medical_Record.Medical_Record_routes import router as medical_record_router
from Prescription.Prescription_routes import router as prescription_router
from Aud_log.AuditLog_routes import router as AuditLog_routes
from Report.Report_routes import router as Report_router

app = FastAPI(
    title="Electronic Medical Records API",
    version="1.0.0"
)
# Register routes
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(role_router, prefix="/roles", tags=["Roles"])
app.include_router(user_role_router, prefix="/user-roles", tags=["User Roles"])
app.include_router(doctor_router, prefix="/doctors", tags=["Doctors"])
app.include_router(AuditLog_routes,prefix="/audit-logs", tags=["Audit Logs"])
app.include_router(Report_router,prefix="/reports", tags=["Reports"])
app.include_router(medical_record_router)
app.include_router(prescription_router)
@app.get("/")
def root():
    return {"status": "EMR Backend running"}
