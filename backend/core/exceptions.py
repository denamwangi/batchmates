"""
Custom exceptions for the BatchMates application.
Provides specific exception types for different error scenarios.
"""
from typing import Optional, Any, Dict


class BatchMatesException(Exception):
    """Base exception for all BatchMates application errors."""
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ProfileNotFoundError(BatchMatesException):
    """Raised when a requested profile is not found."""
    
    def __init__(self, profile_name: str):
        super().__init__(
            message=f"Profile '{profile_name}' not found",
            error_code="PROFILE_NOT_FOUND",
            details={"profile_name": profile_name}
        )


class InterestNotFoundError(BatchMatesException):
    """Raised when a requested interest is not found."""
    
    def __init__(self, interest_name: str):
        super().__init__(
            message=f"Interest '{interest_name}' not found",
            error_code="INTEREST_NOT_FOUND",
            details={"interest_name": interest_name}
        )


class AgentServiceError(BatchMatesException):
    """Raised when the AI agent service fails."""
    
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="AGENT_SERVICE_ERROR",
            details={"original_error": str(original_error) if original_error else None}
        )


class DataValidationError(BatchMatesException):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Optional[Any] = None):
        super().__init__(
            message=message,
            error_code="DATA_VALIDATION_ERROR",
            details={"field": field, "value": str(value) if value is not None else None}
        )


class DataFileError(BatchMatesException):
    """Raised when there's an error reading or writing data files."""
    
    def __init__(self, filename: str, operation: str, original_error: Optional[Exception] = None):
        super().__init__(
            message=f"Failed to {operation} file '{filename}'",
            error_code="DATA_FILE_ERROR",
            details={
                "filename": filename,
                "operation": operation,
                "original_error": str(original_error) if original_error else None
            }
        )


class DatabaseError(BatchMatesException):
    """Raised when there's a database operation error."""
    
    def __init__(self, message: str, operation: str, original_error: Optional[Exception] = None):
        super().__init__(
            message=f"Database error during {operation}: {message}",
            error_code="DATABASE_ERROR",
            details={
                "operation": operation,
                "original_error": str(original_error) if original_error else None
            }
        )


class ConfigurationError(BatchMatesException):
    """Raised when there's a configuration error."""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            details={"config_key": config_key}
        )
