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
            layout: list[RawLayout]
    ):
        return (await self._repo.create(
            name = name,
            theater_id = theater_id,
            layout = layout 
        ))