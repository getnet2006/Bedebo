from fastapi import APIRouter
from app.api.v1.routes import health
from app.api.v1.routes import auth
from app.api.v1.routes import campaigns

api_router = APIRouter()

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)
api_router.include_router(auth.router)
api_router.include_router(campaigns.router)