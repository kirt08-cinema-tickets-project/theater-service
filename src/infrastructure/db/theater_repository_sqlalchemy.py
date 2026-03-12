from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import (
    MultipleResultsFound,
    NoResultFound,
)

from src.domain.repositories.theater_repository import TheaterRepository
from src.domain.entities import TheaterEntity
from src.domain.exceptions.theater import (
    TheaterNotFoundException,
    TheaterNotUniqueException,
)

from src.infrastructure.db.models import TheatersORM



class SQLAlchemyTheaterRepository(TheaterRepository):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def find_all(self) -> list[TheaterEntity]:
        async with self._session_factory() as session:
            data_orm = (await session.execute(
                select(TheatersORM)
                .order_by(TheatersORM.name)
            )).scalars().all()
        res = []
        for row in data_orm:
            res.append(TheaterEntity(
                id = str(row.id),
                name = row.name,
                address = row.address,
                created_at = row.created_at,
                updated_at = row.updated_at  
            ))
        return res
        
    async def find_by_id(self, id: str) -> TheaterEntity:
        async with self._session_factory() as session:
            try:
                data_orm = (await session.execute(
                    select(TheatersORM)
                    .filter_by(id = id)
                )).scalars().one()
            except NoResultFound:
                raise TheaterNotFoundException(f"Theater {id} not found")
            except MultipleResultsFound:
                raise TheaterNotUniqueException(f"Multiple theaters with id {id}")
            return TheaterEntity(
                id = str(data_orm.id),
                name = data_orm.name,
                address = data_orm.address,
                created_at = data_orm.created_at,
                updated_at = data_orm.updated_at 
            )
        
    async def create(self, name, address) -> TheaterEntity:
        async with self._session_factory() as session:
            new_thater = TheatersORM(name = name, address = address)
            session.add(new_thater)
            await session.commit()
            await session.refresh(new_thater)
        return TheaterEntity(
            id = str(new_thater.id),
            name = new_thater.name,
            address = new_thater.address,
            created_at = new_thater.created_at,
            updated_at = new_thater.updated_at  
        )