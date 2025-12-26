from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.models.campaign import Campaign, CampaignStatus
from app.models.user import User
from app.repositories.campaign import (
    create_campaign,
    get_campaign_by_id,
    update_campaign,
)
from app.schemas.campaign import CampaignUpdate
from app.core.exceptions import APIException
from app.core.error_codes import ErrorCode


async def create_new_campaign(
    db: AsyncSession,
    owner: User,
    title: str,
    description: str,
    goal_amount: float,
    deadline: datetime,
) -> Campaign:
    if deadline <= datetime.now(timezone.utc):
        raise APIException(
            status_code=400,
            error_code=ErrorCode.CAMPAIGN_DEADLINE_MUST_BE_FUTURE,
            message="Deadline must be in the future",
        )

    campaign = Campaign(
        owner_id=owner.id,
        title=title,
        description=description,
        goal_amount=goal_amount,
        deadline=deadline,
        status=CampaignStatus.DRAFT,
    )
    return await create_campaign(db, campaign)


async def activate_campaign(
    db: AsyncSession,
    campaign: Campaign,
    owner: User,
) -> Campaign:
    if campaign.owner_id != owner.id:
        raise APIException(
            status_code=401,
            error_code=ErrorCode.CAMPAIGN_NOT_OWNER,
            message="Not campaign owner",
        )

    if campaign.status != CampaignStatus.DRAFT:
        raise APIException(
            status_code=400,
            error_code=ErrorCode.CAMPAIGN_ALREADY_ACTIVE,
            message="Only draft campaigns can be activated",
        )

    campaign.status = CampaignStatus.ACTIVE
    await db.commit()
    await db.refresh(campaign)
    return campaign

async def update_existing_campaign(
    db: AsyncSession,
    campaign: Campaign,
    owner: User,
    updates: CampaignUpdate,
) -> Campaign:
    if campaign.owner_id != owner.id:
        raise APIException(
            status_code=401,
            error_code=ErrorCode.CAMPAIGN_NOT_OWNER,
            message="Not campaign owner",
        )

    if campaign.status != CampaignStatus.DRAFT:
        raise APIException(
            status_code=400,
            error_code=ErrorCode.CAMPAIGN_ALREADY_ACTIVE,
            message="Only draft campaigns can be activated",
        )

    update_data = updates.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(campaign, field, value)

    return await update_campaign(db, campaign)

