import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.db.models.base_model import Base

if TYPE_CHECKING:
    from src.infrastructure.db.models.theaters import TheatersORM
    from src.infrastructure.db.models.seats import SeatsORM


class HallsORM(Base):
    __tablename__ = "halls"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(256))

    theater_id: Mapped[UUID] = mapped_column(ForeignKey("theaters.id"))
    theater_rel: Mapped["TheatersORM"] = relationship(
        back_populates="halls_rel"
    )
    
    seats_rel: Mapped[list["SeatsORM"]] = relationship(
        back_populates="halls_rel"
    )