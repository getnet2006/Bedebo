from fastapi import APIRouter
from app.api.v1.routes import health, auth, campaigns, contributions

api_router = APIRouter()

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)
api_router.include_router(auth.router)
api_router.include_router(campaigns.router)
api_router.include_router(contributions.router)