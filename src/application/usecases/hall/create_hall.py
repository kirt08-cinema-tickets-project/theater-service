from dataclasses import dataclass

from src.domain.repositories import HallRepository


@dataclass
class RawLayout:
    row: int
    columns: int
    type: str
    price: int


class CreateHallUsecase:
    def __init__(self, repo: HallRepository):
        self._repo = repo

    async def execute(
            self,
            name,
            theater_id,
            layouts: list[RawLayout]
    ):
        hall = await self._repo.create(
            name = name,
            theater_id = theater_id,
            layouts = layouts
        )

        await self._repo.create_seats(
            hall_id = hall.id,
            layouts = layouts
        )

        return hall