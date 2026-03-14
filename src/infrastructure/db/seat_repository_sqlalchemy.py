from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from src.domain.entities import SeatEntity
from src.domain.entities.seat import StatusType
from src.domain.repositories import SeatRepository
from src.domain.exceptions import SeatNotFoundException, SeatNotUniqueException

from src.infrastructure.db.models.seats import SeatsORM


class SQLAlchemySeatRepository(SeatRepository):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def find_by_id(self, id: str):
        async with self._session_factory() as session:
            try:
                seat_orm = (await session.execute(
                    select(SeatsORM)
                    .filter_by(id = id)
                )).scalars().one()
            except NoResultFound:
                raise SeatNotFoundException(f"Seat {id} not found")
            except MultipleResultsFound:
                raise SeatNotUniqueException(f"Multiple seats with id {id}")
            
            return SeatEntity(
                id = str(seat_orm.id),
                row = seat_orm.row,
                number = seat_orm.number,
                price = seat_orm.price,
                type = seat_orm.type,
                hall_id = str(seat_orm.hall_id),
                status = StatusType.availible
            )

    async def find_by_hall(self, hall_id: str, screening_id: str):
        async with self._session_factory() as session:
            data_orm = (await session.execute(
                select(SeatsORM)
                .filter_by(hall_id = hall_id)
                .order_by(SeatsORM.row, SeatsORM.number)
            )).scalars().all()
        
        data_dto = [
            SeatEntity(
                id = str(seat.id),
                row = seat.row,
                number = seat.number,
                price = seat.price,
                type = seat.type,
                hall_id = str(seat.hall_id),
                status = StatusType.availible
            )
            for seat in data_orm
        ]
        return data_dto