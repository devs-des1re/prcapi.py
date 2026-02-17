"""Exceptions for the PRC API."""

from __future__ import annotations

__all__ = (
    "PRCException",
    "HTTPException",
    "Forbidden",
    "RateLimited",
    "APIError",
)

class PRCException(Exception):
    """Base exception for all PRC API errors."""

class HTTPException(PRCException):
    """Raised when the API returns an HTTP error."""

    def __init__(self, status: int, message: str, response_data: dict | None = None):
        self.status = status
        self.message = message
        self.response_data = response_data or {}
        super().__init__(f"HTTP {status}: {message}")

class Forbidden(HTTPException):
    """Raised when the Server-Key is invalid or unauthorized (403)."""

    def __init__(self, message: str = "Invalid or unauthorized server key"):
        super().__init__(403, message)

class RateLimited(HTTPException):
    """Raised when rate limited (429). Contains retry_after and bucket."""

    def __init__(self, message: str, retry_after: float, bucket: str | None = None):
        super().__init__(429, message, {"retry_after": retry_after, "bucket": bucket})
        self.retry_after = retry_after
        self.bucket = bucket

class APIError(PRCException):
    """Raised for API-level errors (e.g. 422 no players, 500 Roblox issue)."""

    def __init__(self, message: str, command_id: str | None = None):
        self.command_id = command_id
        super().__init__(message)
