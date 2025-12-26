from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/")
async def health_check():
    return {
        "status": "ok",
        "service": "crowdfunding-api"
    }

@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user
