from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.contribution import (
    ContributionCreate,
    ContributionRead,
)
from app.repositories.campaign import get_campaign_by_id
from app.services.contribution import contribute_to_campaign
from app.repositories.contribution import list_user_contributions

router = APIRouter(prefix="/contributions", tags=["Contributions"])


@router.post(
    "/campaigns/{campaign_id}",
    response_model=ContributionRead,
    status_code=status.HTTP_201_CREATED,
)
async def contribute(
    campaign_id: int,
    contribution_in: ContributionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaign = await get_campaign_by_id(db, campaign_id)
    if not campaign:
        # raise HTTPException(status_code=404, detail="Campaign not found")
        raise APIException(
            status_code=404,
            error_code=ErrorCode.CAMPAIGN_NOT_FOUND,
            message="Campaign not found",
        )

    try:
        return await contribute_to_campaign(
            db=db,
            campaign=campaign,
            contributor=current_user,
            amount=contribution_in.amount,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/me",
    response_model=list[ContributionRead],
)
async def my_contributions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await list_user_contributions(db, current_user.id)