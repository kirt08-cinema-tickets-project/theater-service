from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from src.domain.entities import HallEntity
from src.domain.repositories import HallRepository
from src.domain.exceptions.hall import (
    HallNotFoundException,
    HallNotUniqueException,
)

from src.infrastructure.db.models.halls import HallsORM
from src.infrastructure.db.models.seats import SeatsORM

@dataclass
class RawLayout:
    row: int
    columns: int
    type: str
    price: int


class SQLAlchemyHallRepository(HallRepository):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def create(
        self,
        name,
        theater_id,
        layout: list[RawLayout]
    ):
        async with self._session_factory() as session:
            hall = HallsORM(
                name = name,
                theater_id = theater_id
            )
            session.add(hall)
            await session.commit()
            await session.refresh(hall)
            return HallEntity(
                id = hall.id,
                name = hall.name,
                theater_id = hall.theater_id,
                created_at = hall.created_at,
                updated_at = hall.updated_at 
            )
        
    async def find_by_id(self, id: str):
        async with self._session_factory() as session:
            try:
                hall_orm = (await session.execute(
                    select(HallsORM)
                    .filter_by(id = id)
                )).scalars().one()
            except NoResultFound:
                raise HallNotFoundException(f"Hall {id} not found")
            except MultipleResultsFound:
                raise HallNotUniqueException(f"Multiple halls with id {id}")
            return HallEntity(
                id = hall_orm.id,
                name = hall_orm.name,
                theater_id = hall_orm.theater_id,
                created_at = hall_orm.created_at,
                updated_at = hall_orm.updated_at 
            )
        
    async def list_by_theater(self, theater_id: str):
        async with self._session_factory() as session:
            data_orm = (await session.execute(
                select(HallsORM)
                .filter_by(theater_id = theater_id)
                .order_by(HallsORM.name)
            )).scalars().all()
            data_dto = [
                HallEntity(
                    id = hall.id,
                    name = hall.name,
                    theater_id = hall.theater_id,
                    created_at = hall.created_at,
                    updated_at = hall.updated_at 
                ) for hall in data_orm
            ]
            return data_dto

    async def create_seats(self, hall_id: str, layout: list[RawLayout]):
        seats = []
        for rowConfig in layout:
            for num in range(1, rowConfig.columns):
                seats.append(
                    SeatsORM(
                        row = rowConfig.row,
                        number = num,
                        x = num,
                        y = rowConfig.row,
                        type = rowConfig.type,
                        price = rowConfig.price,
                        hall_id = hall_id,
                    )
                )
        async with self._session_factory() as session:
            session.add_all(seats)
            await session.commit()
