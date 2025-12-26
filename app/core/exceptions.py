from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.error_codes import ErrorCode

class APIException(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        error_code: str,
        message: str,
        details: list | None = None,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details or []


async def api_exception_handler(
    request: Request,
    exc: APIException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            # "details": exc.details,
        },
    )

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=400,  # Or 422 if you prefer
        content={
            "error_code": exc.errors()[0]["type"] if exc.errors() else "invalid_request",
            "details": [exc.errors()[0]["msg"]] if exc.errors() else "Request body is missing or invalid",
        },
    )

async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "error_code": ErrorCode.INTERNAL_ERROR,
            "message": "Internal server error",
            "details": [],
        },
    )

