# visit/routes.py
from .controller import router as visit_router

def register_visit_routes(app):
    app.include_router(
        visit_router,
        prefix="/visits",
        tags=["Visits"]
    )
