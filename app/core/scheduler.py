from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.services.campaign_lifecycle import close_expired_campaigns


scheduler = AsyncIOScheduler()


async def close_campaigns_job():
    async with async_session() as db:
        await close_expired_campaigns(db)


def start_scheduler():
    scheduler.add_job(
        close_campaigns_job,
        trigger="interval",
        minutes=1,
        id="close_expired_campaigns",
        replace_existing=True,
    )
    scheduler.start()
