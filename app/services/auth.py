from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import (
    get_user_by_email,
    create_user,
)
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.models.user import User


async def register_user(
    db: AsyncSession, email: str, password: str
) -> User:
    existing = await get_user_by_email(db, email)
    if existing:
        raise ValueError("User already exists")

    return await create_user(
        db,
        email=email,
        hashed_password=hash_password(password),
    )


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> str:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")

    return create_access_token(subject=str(user.id))
