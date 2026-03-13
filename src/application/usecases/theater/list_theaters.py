from src.domain.entities import TheaterEntity
from src.domain.repositories import TheaterRepository


class ListTheaterUsecase:
    def __init__(self, repo: TheaterRepository):
        self._repo = repo

    async def execute(self) -> TheaterEntity:
        return (await self._repo.find_all())