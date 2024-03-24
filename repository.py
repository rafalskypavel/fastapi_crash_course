from sqlalchemy import select
# Импорт асинхронной сессии базы данных и модели TaskOrm для работы с задачами.
from database import new_session, TaskOrm
# Импорт схем данных для валидации и сериализации.
from schemas import STaskAdd, STask


# Определение класса TaskRepository для работы с задачами в базе данных.
class TaskRepository:
    # Метод класса для добавления новой задачи в базу данных.
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        # Создаем асинхронную сессию базы данных.
        async with new_session() as session:
            # Преобразуем данные задачи в словарь.
            task_dict = data.model_dump()
            # Создаем экземпляр модели TaskOrm на основе полученных данных.
            task = TaskOrm(**task_dict)
            # Добавляем задачу в сессию.
            session.add(task)
            # "Промежуточное" сохранение изменений, но не фиксация транзакции.
            await session.flush()
            # Фиксируем изменения в базе данных (коммит транзакции).
            await session.commit()
            # Возвращаем идентификатор добавленной задачи.
            return task.id

    # Метод класса для поиска всех задач в базе данных.
    @classmethod
    async def find_all(cls) -> list[STask]:
        # Создаем асинхронную сессию базы данных.
        async with new_session() as session:
            # Формируем запрос для выборки всех объектов TaskOrm из базы данных.
            query = select(TaskOrm)
            # Выполняем запрос к базе данных.
            result = await session.execute(query)
            # Получаем список всех объектов задач (TaskOrm).
            task_models = result.scalars().all()
            # Преобразуем объекты задач в соответствующие схемы данных (STask).
            task_schemas = [STask.model_validate(task_model) for task_model in task_models]
            # Возвращаем список всех задач в формате схемы данных STask.
            return task_schemas
