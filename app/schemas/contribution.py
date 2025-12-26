from pydantic import BaseModel, Field
from datetime import datetime


class ContributionCreate(BaseModel):
    amount: float = Field(..., gt=0)


class ContributionRead(BaseModel):
    id: int
    user_id: int
    campaign_id: int
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True
