from app.db import async_session
from app.models import TodoList, Item
from sqlalchemy.future import select
from sqlalchemy import update
from datetime import datetime

class TodoListService:
    def __init__(self, session_factory=async_session):
        # Конструктор сервиса принимает фабрику сессий (по умолчанию async_session)
        self.session_factory = session_factory

    async def get_all(self):
        # Асинхронный метод для получения всех списков дел, которые не удалены deleted_at == None
        async with self.session_factory() as session:
            # Открываем асинхронную сессию с базой данных
            result = await session.execute(
                select(TodoList).where(TodoList.deleted_at == None)
                # Выполняем SELECT запрос к таблице todo_lists
            )
            return result.scalars().all()
            # Получаем список объектов TodoList из результата запроса и возвращаем

    async def soft_delete(self, todo_list_id: int):
        # Асинхронный метод для "мягкого удаления" списка дел по его id
        async with self.session_factory() as session:
            # Открываем асинхронную сессию с базой данных
            await session.execute(
                update(TodoList)
                .where(TodoList.id == todo_list_id)
                # Фильтруем по id списка, который нужно удалить
                .values(deleted_at=datetime.utcnow())
                # Обновляем поле deleted_at на текущее время
            )
            await session.commit()
            # Подтверждаем изменения в базе, чтобы удаление сохранилось
