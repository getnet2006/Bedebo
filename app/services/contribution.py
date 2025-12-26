from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import APIException
from app.core.error_codes import ErrorCode
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
    if campaign.status != CampaignStatus.ACTIVE:
        raise APIException(
            status_code=400,
            error_code=ErrorCode.CAMPAIGN_NOT_ACTIVE,
            message="Campaign is not active",
        )

    if campaign.deadline < datetime.utcnow():
        raise APIException(
            status_code=400,
            error_code=ErrorCode.CAMPAIGN_DEADLINE_PASSED,
            message="Campaign deadline has passed",
        )

    if amount <= 0:
        raise APIException(
            status_code=400,
            error_code=ErrorCode.INVALID_CONTRIBUTION_AMOUNT,
            message="Contribution amount must be greater than zero",
        )

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
