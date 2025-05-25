from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, database_url: str):
        # Создаем асинхронный движок для подключения к базе по переданному URL
        self.engine = create_async_engine(database_url, future=True, echo=True)
        # Создаем фабрику сессий с параметрами
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def get_session(self) -> AsyncSession:
        # Асинхронный генератор сессий для работы с БД
        async with self.async_session() as session:
            yield session
