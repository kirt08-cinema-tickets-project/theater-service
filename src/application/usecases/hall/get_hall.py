from src.domain.repositories import HallRepository


class GetHallUsecase:
    def __init__(self, repo: HallRepository):
        self._repo = repo

    async def execute(
            self,
            id: str
    ):
        return (await self._repo.find_by_id(id = id))