from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.campaign import Campaign


async def create_campaign(
    db: AsyncSession,
    campaign: Campaign,
) -> Campaign:
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    return campaign


async def get_campaign_by_id(
    db: AsyncSession,
    campaign_id: int,
) -> Campaign | None:
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id)
    )
    return result.scalar_one_or_none()


async def list_active_campaigns(
    db: AsyncSession,
) -> list[Campaign]:
    result = await db.execute(
        select(Campaign).where(Campaign.status == "ACTIVE")
    )
    return result.scalars().all()

async def update_campaign(
    db: AsyncSession,
    campaign: Campaign,
) -> Campaign:
    await db.commit()
    await db.refresh(campaign)
    return campaign

async def get_campaign_for_update(db, campaign_id: int):
    result = await db.execute(
        select(Campaign)
        .where(Campaign.id == campaign_id)
        .with_for_update()
    )
    return result.scalar_one_or_none()
