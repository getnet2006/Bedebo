from sqlalchemy import String, Text, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum

from app.db.base import Base


class CampaignStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    goal_amount: Mapped[float] = mapped_column(Numeric(12, 2))
    current_amount: Mapped[float] = mapped_column(
        Numeric(12, 2), default=0
    )

    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    status: Mapped[CampaignStatus] = mapped_column(
        Enum(CampaignStatus),
        default=CampaignStatus.DRAFT,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    owner = relationship("User", back_populates="campaigns")
    contributions = relationship(
        "Contribution",
        back_populates="campaign",
        cascade="all, delete-orphan",
    )
