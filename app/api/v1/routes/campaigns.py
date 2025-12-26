from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.campaign import (
    CampaignCreate,
    CampaignRead,
)
from app.services.campaign import create_new_campaign
from app.repositories.campaign import (
    get_campaign_by_id,
    list_active_campaigns,
)
from app.schemas.campaign import CampaignUpdate
from app.services.campaign import update_existing_campaign
from app.repositories.campaign import update_campaign
from app.api.deps import get_current_user_optional
from app.models.campaign import CampaignStatus
from app.services.campaign import activate_campaign
from typing import Optional
from app.core.exceptions import APIException
from app.core.error_codes import ErrorCode


router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post(
    "/",
    response_model=CampaignRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_campaign(
    campaign_in: CampaignCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await create_new_campaign(
            db=db,
            owner=current_user,
            **campaign_in.dict(),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CampaignRead])
async def list_campaigns(
    db: AsyncSession = Depends(get_db),
):
    return await list_active_campaigns(db)


@router.get("/{campaign_id}", response_model=CampaignRead)
async def get_campaign(
    campaign_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    campaign = await get_campaign_by_id(db, campaign_id)
    if not campaign:
        # raise HTTPException(status_code=404, detail="Campaign not found")
        raise APIException(
            status_code=404,
            error_code=ErrorCode.CAMPAIGN_NOT_FOUND,
            message="Campaign not found",
        )

    # PUBLIC: ACTIVE campaigns
    if campaign.status == CampaignStatus.ACTIVE:
        return campaign

    # PRIVATE: DRAFT or CLOSED
    if not current_user or campaign.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to view this campaign",
        )

    return campaign

@router.put(
    "/{campaign_id}",
    response_model=CampaignRead,
)
async def update_campaign_endpoint(
    campaign_id: int,
    campaign_in: CampaignUpdate,
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
        return await update_existing_campaign(
            db=db,
            campaign=campaign,
            owner=current_user,
            updates=campaign_in,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/{campaign_id}/activate",
    response_model=CampaignRead,
)
async def activate_campaign_endpoint(
    campaign_id: int,
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
        return await activate_campaign(
            db=db,
            campaign=campaign,
            owner=current_user,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
