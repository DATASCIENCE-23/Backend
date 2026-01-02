from fastapi import FastAPI

# Import routers
from User.User_routes import router as user_router
from Role.Role_routes import router as role_router
from User_Role.User_Role_routes import router as user_role_router
from Medical_Record.Medical_Record_routes import router as medical_record_router


app = FastAPI(
    title="Electronic Medical Records API",
    version="1.0.0"
)

# Register routes
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(role_router, prefix="/roles", tags=["Roles"])
app.include_router(user_role_router, prefix="/user-roles", tags=["User Roles"])
app.include_router(medical_record_router)


@app.get("/")
def root():
    return {"status": "EMR Backend running"}
