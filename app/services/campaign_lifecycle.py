from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.campaign import Campaign, CampaignStatus


async def close_expired_campaigns(db: AsyncSession) -> int:
    """
    Closes all ACTIVE campaigns whose deadline has passed.
    Returns number of campaigns closed.
    """
    result = await db.execute(
        select(Campaign)
        .where(Campaign.status == CampaignStatus.ACTIVE)
        .where(Campaign.deadline < datetime.utcnow())
    )

    campaigns = result.scalars().all()

    for campaign in campaigns:
        campaign.status = CampaignStatus.CLOSED

    if campaigns:
        await db.commit()

    return len(campaigns)
