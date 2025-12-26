from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.contribution import Contribution


async def create_contribution(
    db: AsyncSession,
    contribution: Contribution,
) -> Contribution:
    db.add(contribution)
    await db.commit()
    await db.refresh(contribution)
    return contribution


async def list_user_contributions(
    db: AsyncSession,
    user_id: int,
) -> list[Contribution]:
    result = await db.execute(
        select(Contribution).where(Contribution.user_id == user_id)
    )
    return result.scalars().all()
