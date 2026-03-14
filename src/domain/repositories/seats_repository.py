from typing import Protocol

from src.domain.entities import SeatEntity


class SeatRepository(Protocol):
    async def find_by_id(self, id: str) -> SeatEntity: 
        ...

    async def find_by_hall(self, hall_id: str, screening_id: str) -> list[SeatEntity]:
        ...