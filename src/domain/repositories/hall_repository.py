from typing import Protocol
from dataclasses import dataclass

from src.domain.entities import HallEntity


@dataclass
class RawLayout:
    row: int
    columns: int
    type: str
    price: int


class HallRepository(Protocol):
    async def create(
            self,
            name,
            theater_id,
            layouts: list[RawLayout]
    ) -> HallEntity:
        ...

    async def find_by_id(self, id: str) -> HallEntity | None:
        ...

    async def list_by_theater(self, theater_id: str) -> list[HallEntity]:
        ...
    
    async def create_seats(self, hall_id: str, layouts: list[RawLayout]) -> None:
        ...