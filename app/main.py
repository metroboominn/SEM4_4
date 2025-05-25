import os
from fastapi import FastAPI
from app.database import Database
from app.services import TodoListService
from app.views import TodoListView
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# Получаем строку подключения к базе данных из переменных окружения

def create_app() -> FastAPI:
    app = FastAPI()
    db = Database(DATABASE_URL)

    todo_service = TodoListService(db)
    # Создаем сервис для работы с TodoList, передаем объект базы данных

    todo_view = TodoListView(todo_service, db)
    # Создаем объект представления, передаем сервис и объект базы данных

    app.include_router(todo_view.router, prefix="/todo_lists", tags=["TodoLists"])
    # Регистрируем роутер из представления в основном приложении под префиксом /todo_lists

    return app
    # Возвращаем готовое приложение FastAPI

app = create_app()
# Вызываем функцию создания приложения и сохраняем результат в переменную app
