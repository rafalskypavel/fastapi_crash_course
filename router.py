from typing import Annotated

# Импорт класса TaskRepository из модуля repository для работы с задачами в базе данных.
from repository import TaskRepository

# Импорт схем STaskAdd, STask, STaskId из модуля schemas для валидации и сериализации данных.
from schemas import STaskAdd, STask, STaskId

# Импорт класса APIRouter из библиотеки FastAPI для создания маршрутов API.
from fastapi import APIRouter, Depends

# Создаем экземпляр APIRouter, который представляет собой группу маршрутов API, связанных с задачами.
# Указываем префикс URI "/tasks", который будет добавляться ко всем маршрутам в группе, например, "/tasks/add" или "/tasks/get".
# Это помогает организовать логическую группировку маршрутов и упрощает их поддержку и обслуживание.
# Тег "Таски" используется для документации Swagger, что позволяет легко найти и описать группу маршрутов, связанных с задачами, в API-документации.
router = APIRouter(
    prefix="/tasks",  # Префикс URI для всех маршрутов в группе.
    tags=["Таски"],  # Тег для документации Swagger.
)


# Обработчик POST-запроса для добавления новой задачи.
@router.post("")
async def add_task(
    task: Annotated[STaskAdd, Depends()],  # Параметр запроса с аннотацией STaskAdd для валидации.
) -> STaskId:
    # Вызываем метод add_one() класса TaskRepository для добавления задачи в базу данных.
    task_id = await TaskRepository.add_one(task)
    # Возвращаем ответ с идентификатором добавленной задачи.
    return {"ok": True, "task_id": task_id}

# Обработчик GET-запроса для получения списка всех задач.
@router.get("")
async def get_tasks() -> list[STask]:
    # Получаем список всех задач из базы данных с помощью метода find_all() класса TaskRepository.
    tasks = await TaskRepository.find_all()
    # Возвращаем список задач в ответ на GET-запрос.
    return tasks
