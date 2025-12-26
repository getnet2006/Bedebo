from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

def is_missing_body(errors):
    return any(
        err["loc"] == ["body"] and err["type"] == "missing"
        for err in errors
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
