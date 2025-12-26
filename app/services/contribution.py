from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contribution import Contribution
from app.models.campaign import Campaign, CampaignStatus
from app.models.user import User
import decimal

async def contribute_to_campaign(
    db: AsyncSession,
    campaign: Campaign,
    contributor: User,
    amount: float,
) -> Contribution:
    # 1. Campaign must be ACTIVE
    if campaign.status != CampaignStatus.ACTIVE:
        raise ValueError("Campaign is not active")

    # 2. Deadline enforcement
    if campaign.deadline < datetime.utcnow():
        raise ValueError("Campaign deadline has passed")

    # 3. Create contribution
    contribution = Contribution(
        user_id=contributor.id,
        campaign_id=campaign.id,
        amount=amount,
    )

    # 4. Update campaign total atomically
    campaign.current_amount += decimal.Decimal(amount)

    db.add(contribution)
    await db.commit()
    await db.refresh(contribution)

    return contribution
