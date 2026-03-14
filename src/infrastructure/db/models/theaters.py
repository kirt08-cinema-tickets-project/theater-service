import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.db.models.base_model import Base

if TYPE_CHECKING:
    from src.infrastructure.db.models.halls import HallsORM


class TheatersORM(Base):
    __tablename__ = "theaters"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    address: Mapped[str] = mapped_column(String(256), nullable=False)

    halls_rel: Mapped[list["HallsORM"]] = relationship(
        back_populates="theater_rel",
        cascade="all, delete-orphan"
    )