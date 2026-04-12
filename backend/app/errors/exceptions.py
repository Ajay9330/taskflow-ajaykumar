from typing import Any, Dict, Optional

class AppError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class NotFoundError(AppError):
    pass

class ForbiddenError(AppError):
    pass

class UnauthorizedError(AppError):
    pass

class ValidationError(AppError):
    def __init__(self, message: str, fields: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.fields = fields
