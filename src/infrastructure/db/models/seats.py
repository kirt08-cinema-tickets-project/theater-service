import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.db.models.base_model import Base

if TYPE_CHECKING:
    from src.infrastructure.db.models.halls import HallsORM


class SeatsORM(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    row: Mapped[int]
    number: Mapped[int]
    x: Mapped[int]
    y: Mapped[int]
    type: Mapped[str] = mapped_column(String(256))
    price: Mapped[int]

    hall_id: Mapped[UUID] = mapped_column(ForeignKey("halls.id"))
    halls_rel: Mapped["HallsORM"] = relationship(
        back_populates="seats_rel",
        cascade="all, delete-orphan"
    )