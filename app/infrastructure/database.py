from __future__ import annotations

from typing import AsyncIterator, Optional
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import text
from sqlalchemy.pool import AsyncAdaptedQueuePool
from app.config.settings import Settings


class SessionManager:
    """Manages asynchronous DB sessions with connection pooling."""

    def __init__(self, settings: Settings) -> None:
        self.engine: Optional[AsyncEngine] = None
        self._sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None
        self.settings = settings
        self.init_db()

    def init_db(self) -> None:
        """Initialize the database engine and session factory."""
        self.engine = create_async_engine(
            url=self.settings.get_database_url,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=self.settings.POOL_SIZE,
            max_overflow=self.settings.MAX_OVERFLOW,
            pool_pre_ping=True,
            pool_recycle=self.settings.POOL_RECYCLE,
            echo=self.settings.DATABASE_DEBUG,
            # echo_pool="debug",
        )

        self._sessionmaker = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )

    async def connect(self) -> bool:
        """Check connection."""
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            return False

    async def close(self) -> None:
        """Dispose of the database engine."""
        if self.engine:
            await self.engine.dispose()

    @asynccontextmanager
    async def async_generator(self) -> AsyncIterator[AsyncSession]:

        if not self._sessionmaker:
            raise RuntimeError("Database session factory is not initialized.")

        session = self._sessionmaker()
        try:
            yield session

            # await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.aclose()
