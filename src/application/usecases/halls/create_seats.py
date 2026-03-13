from dataclasses import dataclass

from src.domain.repositories import HallRepository


@dataclass
class RawLayout:
    row: int
    columns: int
    type: str
    price: int


class CreateSeatsUsecase:
    def __init__(self, repo: HallRepository):
        self._repo = repo

    async def execute(self, hall_id: str, layout: list[RawLayout]):
        return (await self._repo.create_seats(
            self, 
            hall_id = hall_id,
            layout = layout
        ))