import asyncio
import logging

from src.infrastructure.config import settings

from src.infrastructure.db.database import db

from src.infrastructure.db.theater_repository_sqlalchemy import SQLAlchemyTheaterRepository
from src.infrastructure.db.hall_repository_sqlalchemy import SQLAlchemyHallRepository
from src.infrastructure.db.seat_repository_sqlalchemy import SQLAlchemySeatRepository

from src.application.usecases.theater import(
    CreateTheaterUsecase,
    GetTheaterUsecase,
    ListTheaterUsecase,
)

from src.application.usecases.hall import (
    GetHallUsecase,
    ListHallUsecase,
    CreateHallUsecase,
)

from src.application.usecases.seat import (
    GetSeatUsecase,
    ListSeatUsecase,
)

from src.presentation.grpc.server import serve
from src.presentation.grpc.theater_controller import TheaterGrpcController
from src.presentation.grpc.hall_controller import HallGrpcController
from src.presentation.grpc.seat_controller import SeatGrpcController


logging.basicConfig(
        format=settings.logger.format, 
        level=settings.logger.log_level   
    )

async def main():
    # Theater
    theater_repo = SQLAlchemyTheaterRepository(db.sessionmaker)

    theater_create_usecase = CreateTheaterUsecase(repo = theater_repo)
    theater_get_usecase = GetTheaterUsecase(repo = theater_repo)
    theater_list_usecase = ListTheaterUsecase(repo = theater_repo)

    theater_controller = TheaterGrpcController(
        create_usecase = theater_create_usecase,
        get_usecase = theater_get_usecase,
        list_usecase = theater_list_usecase 
    )

    # Hall
    hall_repo = SQLAlchemyHallRepository(db.sessionmaker)

    hall_create_hall_usecase = CreateHallUsecase(repo = hall_repo)
    hall_get_usecase = GetHallUsecase(repo = hall_repo)
    hall_list_usecase = ListHallUsecase(repo = hall_repo)
    
    hall_controller = HallGrpcController(
        create_hall_usecase = hall_create_hall_usecase,
        get_hall_usecase = hall_get_usecase,
        list_hall_usecase = hall_list_usecase,
    )

    # Seats
    seats_repo = SQLAlchemySeatRepository(db.sessionmaker)

    seat_get_usecase = GetSeatUsecase(repo = seats_repo)
    seat_list_usecase = ListSeatUsecase(repo = seats_repo)
    
    seat_controller = SeatGrpcController(
        get_seat_usecase = seat_get_usecase,
        list_seat_usecase = seat_list_usecase,
    )


    await serve(
        theater_controller = theater_controller,
        hall_controller = hall_controller,
        seat_controller = seat_controller
    )

if __name__ == "__main__":
    asyncio.run(main())