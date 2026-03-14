from src.domain.entities import SeatEntity
from src.domain.repositories import SeatRepository


class ListSeatUsecase:
    def __init__(self, repo: SeatRepository):
        self._repo = repo

    async def execute(
            self,
            hall_id: str,
            screening_id: str
    ):
        seats = await self._repo.find_by_hall(
            hall_id = hall_id,
            screening_id = screening_id
        )
        return seats