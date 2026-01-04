"""
Routes Layer
API endpoint definitions for Lab Scheduling module
"""

from .lab_order_routes import router as lab_order_routes
from .lab_schedule_routes import router as lab_schedule_routes
from .lab_result_routes import router as lab_result_routes
from .lab_report_routes import router as lab_report_routes

__all__ = [
    "lab_order_routes",
    "lab_schedule_routes",
    "lab_result_routes",
    "lab_report_routes"
]