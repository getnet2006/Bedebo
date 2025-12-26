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


async def create_new_campaign(
    db: AsyncSession,
    owner: User,
    title: str,
    description: str,
    goal_amount: float,
    deadline: datetime,
) -> Campaign:
    if deadline <= datetime.now(timezone.utc):
        raise ValueError("Deadline must be in the future")

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
        raise PermissionError("Not campaign owner")

    if campaign.status != CampaignStatus.DRAFT:
        raise ValueError("Only draft campaigns can be activated")

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
        raise PermissionError("Not campaign owner")

    if campaign.status != CampaignStatus.DRAFT:
        raise ValueError("Only draft campaigns can be updated")

    update_data = updates.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(campaign, field, value)

    return await update_campaign(db, campaign)

