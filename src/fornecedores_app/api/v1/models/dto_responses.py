from pydantic import BaseModel

from typing import (
    Generic,
    List,
    Optional,
    TypeVar,
)

T = TypeVar("T")


class PageMeta(BaseModel):
    page: int
    per_page: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "page": 1,
                "per_page": 5,
                "total_items": 10,
                "total_pages": 2,
                "has_next": True,
                "has_previous": False,
            }
        }
    }


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: PageMeta


class ErrorResponse(BaseModel):
    pass


class Error400Response(ErrorResponse):
    status_code: int = 400
    error: str = "Bad Request"
    message: str
    path: Optional[str]
    timestamp: Optional[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "status_code": 400,
                "error": "Bad Request",
                "message": "Invalid request",
                "path": "/api/v1/",
                "timestamp": "2025-10-28T16:02:00Z",
            }
        }
    }


class Error403Response(ErrorResponse):
    status_code: int = 403
    error: str = "Forbidden"
    message: str
    path: Optional[str]
    timestamp: Optional[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "status_code": 403,
                "error": "Forbidden",
                "message": "Operation not allowed in the current resource state",
                "path": "/api/v1/",
                "timestamp": "2025-10-28T16:02:00Z",
            }
        }
    }


class Error404Response(ErrorResponse):
    status_code: int = 404
    error: str = "Not Found"
    message: str
    path: Optional[str]
    timestamp: Optional[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "status_code": 404,
                "error": "Not Found",
                "message": "Resource not found",
                "path": "/api/v1/",
                "timestamp": "2025-10-28T16:02:00Z",
            }
        }
    }


class Error422Response(ErrorResponse):
    status_code: int = 422
    error: str = "Unprocessable Entity"
    message: str
    path: Optional[str]
    timestamp: Optional[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "status_code": 422,
                "error": "Unprocessable Entity",
                "message": "Invalid request payload",
                "path": "/api/v1/",
                "timestamp": "2025-10-28T16:02:00Z",
                "data": {
                    "field": "value",
                    "field2": "value2",
                },
            }
        }
    }


class Error409Response(ErrorResponse):
    status_code: int = 409
    error: str = "Conflict"
    message: str
    path: Optional[str]
    timestamp: Optional[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "status_code": 409,
                "error": "Conflict",
                "message": "Resource already exists",
                "path": "/api/v1/",
                "timestamp": "2025-10-28T16:02:00Z",
            }
        }
    }
