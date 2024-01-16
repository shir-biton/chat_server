from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from server.app_config import settings
from server.utils import Singleton


class AsyncDatabaseSession(metaclass=Singleton):
    def __init__(self):
        self.async_session = None
        self.engine = create_async_engine(settings.db_url, future=True)

    async def init_db(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def get_db(self) -> AsyncSession:
        try:
            self.async_session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
            async with self.async_session() as session:
                yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.flush()
            await session.close()


database = AsyncDatabaseSession()
