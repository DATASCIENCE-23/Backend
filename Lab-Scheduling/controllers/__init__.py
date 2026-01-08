"""
Controller Layer
HTTP request handling for Lab Scheduling module
"""

from .lab_order_controller import LabOrderController
from .lab_schedule_controller import LabScheduleController
from .lab_result_controller import LabResultController
from .lab_report_controller import LabReportController

__all__ = [
    "LabOrderController",
    "LabScheduleController",
    "LabResultController",
    "LabReportController"
]