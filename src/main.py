import asyncio
import logging

from src.infrastructure.config import settings
from src.infrastructure.db.theater_repository_sqlalchemy import SQLAlchemyTheaterRepository
from src.infrastructure.db.database import db

from src.application.usecases.theater import(
    CreateTheaterUsecase,
    GetTheaterUsecase,
    ListTheaterUsecase,
)

from src.presentation.grpc.server import serve


logging.basicConfig(
        format=settings.logger.format, 
        level=settings.logger.log_level   
    )

async def main():
    repo = SQLAlchemyTheaterRepository(db.sessionmaker)

    create_usecase = CreateTheaterUsecase(repo = repo)
    get_usecase = GetTheaterUsecase(repo = repo)
    list_usecase = ListTheaterUsecase(repo = repo)

    await serve(
        create_usecase = create_usecase,
        get_usecase = get_usecase,
        list_usecase = list_usecase
    )

if __name__ == "__main__":
    asyncio.run(main())