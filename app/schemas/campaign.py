from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class CampaignStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class CampaignCreate(BaseModel):
    title: str
    description: str
    goal_amount: float
    deadline: datetime


class CampaignUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: datetime | None = None
    goal_amount: float | None = None


class CampaignRead(BaseModel):
    id: int
    title: str
    description: str
    goal_amount: float
    current_amount: float
    deadline: datetime
    status: CampaignStatus
    owner_id: int

    class Config:
        from_attributes = True
