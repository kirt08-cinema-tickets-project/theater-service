from src.domain.entities import TheaterEntity
from src.domain.repositories import TheaterRepository


class GetTheaterUsecase:
    def __init__(self, repo: TheaterRepository):
        self._repo = repo

    async def execute(self, id: str) -> TheaterEntity:
        return (await self._repo.find_by_id(id = id))
        
        