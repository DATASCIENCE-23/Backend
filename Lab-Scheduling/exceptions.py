"""
Custom Exceptions for Lab Scheduling Module
Defines specific exceptions for different error scenarios
"""

class LabSchedulingException(Exception):
    """Base exception for lab scheduling module"""
    def __init__(self, message: str, code: str = "LAB_SCHEDULING_ERROR", details: str = None):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        return self.message


class LabOrderNotFoundException(LabSchedulingException):
    """Exception raised when lab order is not found"""
    def __init__(self, message: str = "Lab order not found"):
        super().__init__(
            message=message,
            code="LAB_ORDER_NOT_FOUND",
            details="The requested lab order does not exist in the system"
        )


class LabScheduleNotFoundException(LabSchedulingException):
    """Exception raised when lab schedule is not found"""
    def __init__(self, message: str = "Lab schedule not found"):
        super().__init__(
            message=message,
            code="LAB_SCHEDULE_NOT_FOUND",
            details="The requested lab schedule does not exist in the system"
        )


class LabResultNotFoundException(LabSchedulingException):
    """Exception raised when lab result is not found"""
    def __init__(self, message: str = "Lab result not found"):
        super().__init__(
            message=message,
            code="LAB_RESULT_NOT_FOUND",
            details="The requested lab result does not exist in the system"
        )


class LabReportNotFoundException(LabSchedulingException):
    """Exception raised when lab report is not found"""
    def __init__(self, message: str = "Lab report not found"):
        super().__init__(
            message=message,
            code="LAB_REPORT_NOT_FOUND",
            details="The requested lab report does not exist in the system"
        )


class ResultValidationException(LabSchedulingException):
    """Exception raised when result validation fails"""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="RESULT_VALIDATION_ERROR",
            details="The lab result failed validation checks"
        )


class ReportFinalizedException(LabSchedulingException):
    """Exception raised when trying to modify a finalized report"""
    def __init__(self, message: str = "Report is already finalized"):
        super().__init__(
            message=message,
            code="REPORT_FINALIZED",
            details="Finalized reports cannot be modified"
        )


class InvalidScheduleTimeException(LabSchedulingException):
    """Exception raised when schedule time is invalid"""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="INVALID_SCHEDULE_TIME",
            details="The scheduled time is invalid or conflicts with business rules"
        )


class ScheduleConflictException(LabSchedulingException):
    """Exception raised when there's a scheduling conflict"""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="SCHEDULE_CONFLICT",
            details="The requested schedule conflicts with existing appointments"
        )


class DatabaseConnectionException(LabSchedulingException):
    """Exception raised when database connection fails"""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="DATABASE_CONNECTION_ERROR",
            details="Failed to connect to the database"
        )


class AuthenticationException(LabSchedulingException):
    """Exception raised when authentication fails"""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            details="Valid authentication credentials are required"
        )


class AuthorizationException(LabSchedulingException):
    """Exception raised when authorization fails"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            details="User does not have sufficient permissions for this operation"
        )