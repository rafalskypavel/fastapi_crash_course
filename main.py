from contextlib import asynccontextmanager
from fastapi import FastAPI
# Импорт функций создания и удаления таблиц из модуля database.
from database import create_tables, delete_tables
# Импорт маршрута для задач из модуля router.
from router import router as tasks_router


# Определение контекстного менеджера для управления жизненным циклом приложения.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Удаление таблиц перед запуском приложения.
    await delete_tables()
    print("База данных очищена")
    # Создание таблиц при запуске приложения.
    await create_tables()
    print("База данных готова к работе")
    # Возвращаем контекст приложения для использования внутри блока контекста.
    yield
    # Код после yield выполняется при выходе из блока контекста.
    print("Выключение")


# Создание экземпляра FastAPI с использованием контекстного менеджера lifespan.
app = FastAPI(lifespan=lifespan)
# Включение маршрута для задач в приложение.
app.include_router(tasks_router)
