from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import engine
from app.db.base import Base

# This line is mandatory for table creation
import app.models  # noqa

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)
