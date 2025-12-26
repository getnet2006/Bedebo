
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, db: AsyncSession):
    response = await client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "test@example.com"
    assert "id" in user
