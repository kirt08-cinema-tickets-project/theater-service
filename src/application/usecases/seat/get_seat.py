from src.domain.repositories import SeatRepository


class GetSeatUsecase:
    def __init__(self, repo: SeatRepository):
        self._repo = repo

    async def execute(
            self,
            id: str
    ):
        return (await self._repo.find_by_id(id = id))