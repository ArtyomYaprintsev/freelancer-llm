from decimal import Decimal
from enum import IntEnum
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from project.database import Base


class Freelancer(Base):
    __tablename__ = "freelancers"

    class ProjectType(IntEnum):
        Fixed = 0
        Hourly = 1

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    job_category: Mapped[str] = mapped_column(sa.String(100), index=True)
    platform: Mapped[str] = mapped_column(sa.String(100), index=True)
    experience_level: Mapped[str] = mapped_column(sa.String(100), index=True)
    client_region: Mapped[str] = mapped_column(sa.String(100), index=True)
    payment_method: Mapped[str] = mapped_column(sa.String(100), index=True)
    job_completed: Mapped[int] = mapped_column(sa.SmallInteger())
    earnings_USD: Mapped[int] = mapped_column(sa.SmallInteger())
    hourly_rate: Mapped[Decimal] = mapped_column(sa.Numeric(6, 2))
    job_success_rate: Mapped[Decimal] = mapped_column(sa.Numeric(5, 2))
    client_ration: Mapped[Decimal] = mapped_column(sa.Numeric(5, 2))
    job_duration_days: Mapped[int] = mapped_column(sa.SmallInteger())
    project_type: Mapped[ProjectType] = mapped_column(index=True)
    rehire_rate: Mapped[Decimal] = mapped_column(sa.Numeric(5, 2))
    marketing_spend: Mapped[int] = mapped_column(sa.SmallInteger())
