from typing import Optional

# Импорт необходимых модулей из библиотеки SQLAlchemy для работы с асинхронными запросами
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Создание асинхронного движка для работы с базой данных SQLite.
# Преимущество использования асинхронного движка в том, что он позволяет выполнять запросы к базе данных
# без блокирования основного потока выполнения программы, что особенно важно в асинхронных приложениях.
engine = create_async_engine(
    "sqlite+aiosqlite:///tasks.db"
)

# Создание асинхронного сессионного класса, который будет использоваться для взаимодействия с базой данных.
new_session = async_sessionmaker(engine, expire_on_commit=False)

# Определение базовой модели, от которой будут наследоваться все модели в приложении.
class Model(DeclarativeBase):
    pass


# Определение модели TaskOrm, которая отображает таблицу "tasks" в базе данных.
class TaskOrm(Model):
    __tablename__ = "tasks"

    # Определение столбцов таблицы "tasks" с их типами данных.
    # Mapped - обобщенный тип данных, который оборачивает типы данных SQLAlchemy и позволяет указывать типы данных атрибутов модели.
    # В данном случае, id - целочисленный столбец, который является первичным ключом.
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]  # Строковый столбец для названия задачи.
    description: Mapped[Optional[str]]  # Строковый столбец для описания задачи (может быть пустым).

# Асинхронная функция для создания таблиц в базе данных.
async def create_tables():
    # Устанавливаем соединение с базой данных.
    async with engine.begin() as conn:
        # Асинхронно создаем все таблицы, определенные в метаданных.
        await conn.run_sync(Model.metadata.create_all)

# Асинхронная функция для удаления таблиц из базы данных.
async def delete_tables():
    # Устанавливаем соединение с базой данных.
    async with engine.begin() as conn:
        # Асинхронно удаляем все таблицы, определенные в метаданных.
        await conn.run_sync(Model.metadata.drop_all)
