from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas import TodoListCreate, TodoListInDB, TodoListUpdate
from app.services import TodoListService
from app.database import Database


class TodoListView:
    def __init__(self, service: TodoListService, db: Database):
        # Сохраняем ссылку на сервис, который содержит бизнес-логику по работе со списками дел
        self.service = service
        # Сохраняем объект базы данных для получения сессий
        self.db = db
        # Создаем роутер FastAPI — это набор URL-эндпоинтов для TodoList
        self.router = APIRouter()
        # Регистрируем маршруты и связываем их с методами класса
        self.router.add_api_route("/", self.get_all, methods=["GET"], response_model=List[TodoListInDB])
        # Получить один список дел по ID
        self.router.add_api_route("/{list_id}", self.get_by_id, methods=["GET"], response_model=TodoListInDB)
        # Создать новый список дел
        self.router.add_api_route("/", self.create, methods=["POST"], response_model=TodoListInDB)
        # Частично обновить список дел по ID
        self.router.add_api_route("/{list_id}", self.update, methods=["PATCH"], response_model=TodoListInDB)
        # Мягко удалить список дел по ID
        self.router.add_api_route("/{list_id}", self.delete, methods=["DELETE"])

    async def get_db_session(self):
        # Асинхронный генератор, который возвращает сессию базы данных
        async for session in self.db.get_session():
            yield session

    async def get_all(self, session: AsyncSession = Depends(get_db_session)):
        # Получить все списки дел из базы через сервис
        return await self.service.get_all(session)

    async def get_by_id(self, list_id: int, session: AsyncSession = Depends(get_db_session)):
        # Получить один список дел по ID через сервис
        todo = await self.service.get_by_id(session, list_id)
        if not todo:
            # Если не найден — вернуть ошибку 404
            raise HTTPException(status_code=404, detail="TodoList not found")
        return todo

    async def create(self, todo_data: TodoListCreate, session: AsyncSession = Depends(get_db_session)):
        # Создать новый список дел, используя данные из запроса и сервис
        return await self.service.create(session, todo_data)

    async def update(self, list_id: int, todo_data: TodoListUpdate, session: AsyncSession = Depends(get_db_session)):
        # Здесь должна быть логика частичного обновления списка дел
        # Например, вызвать сервис для обновления и вернуть обновленный объект
        pass

    async def delete(self, list_id: int, session: AsyncSession = Depends(get_db_session)):
        # Мягко удалить список дел (установить deleted_at)
        await self.service.soft_delete(session, list_id)
        # Вернуть простое сообщение об успешном удалении
        return {"detail": "Deleted"}
