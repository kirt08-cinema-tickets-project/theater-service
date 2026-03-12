from typing import Protocol

from src.domain.entities import TheaterEntity

class TheaterRepository(Protocol):
    async def find_all(self) -> list[TheaterEntity]:
        ...

    async def find_by_id(self, id: str) -> TheaterEntity:
        ...

    async def create(self, name: str, address: str) -> TheaterEntity:
        ...