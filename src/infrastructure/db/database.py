from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.infrastructure.config import settings

class DataBase:
    def __init__(self, url: str = "", echo: bool = False):
        self._url: URL = url
        self._echo: bool = echo

        self._engine = None
        self._session = None 

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_async_engine(
                url = self._url,
                echo = self._echo
            )
        return self._engine
    
    @property
    def sessionmaker(self):
        if self._session is None:
            self._session = async_sessionmaker(
                bind = self.engine,
                expire_on_commit = False
            )
        return self._session
    
    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self.sessionmaker() as session:
            yield session

db = DataBase(
    url = settings.db.async_url,
    echo = settings.db.echo
)