class AIConsultancyMonitorException(Exception):
    """Base exception for the application."""

    def __init__(self, message: str = None, status_code: int = 500):
        self.message = message or "An error occurred"
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AIConsultancyMonitorException):
    """Resource not found."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} not found", status_code=404)


class ValidationException(AIConsultancyMonitorException):
    """Validation error."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class ExternalAPIException(AIConsultancyMonitorException):
    """External API error."""

    def __init__(self, service: str, message: str = None):
        super().__init__(
            message or f"Error communicating with {service}",
            status_code=502,
        )


class RateLimitException(AIConsultancyMonitorException):
    """Rate limit exceeded."""

    def __init__(self):
        super().__init__("Rate limit exceeded", status_code=429)


class DiagnosisException(AIConsultancyMonitorException):
    """Diagnosis processing error."""

    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class SignalProcessingException(AIConsultancyMonitorException):
    """Signal processing error."""

    def __init__(self, message: str):
        super().__init__(message, status_code=500)
