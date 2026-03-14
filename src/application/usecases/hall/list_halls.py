from src.domain.repositories import HallRepository


class ListHallUsecase:
    def __init__(self, repo: HallRepository):
        self._repo = repo

    async def execute(
            self,
            theater_id: str
    ):
        return (await self._repo.list_by_theater(theater_id = theater_id))