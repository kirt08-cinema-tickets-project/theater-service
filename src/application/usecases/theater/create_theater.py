from src.domain.entities import TheaterEntity
from src.domain.repositories import TheaterRepository


class CreateTheaterUsecase:
    def __init__(self, repo: TheaterRepository):
        self._repo = repo

    async def execute(self, name: str, address: str) -> TheaterEntity:
        return (await self._repo.create(name = name, address = address))
        