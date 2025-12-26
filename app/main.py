from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.router import api_router
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import validation_exception_handler, api_exception_handler, unhandled_exception_handler, APIException    
from app.core.scheduler import start_scheduler


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

@app.on_event("startup")
async def startup_event():
    start_scheduler()

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)

app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
