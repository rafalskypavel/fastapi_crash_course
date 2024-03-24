from typing import Optional
from pydantic import BaseModel


# Определение схемы данных для добавления новой задачи.
class STaskAdd(BaseModel):
    name: str  # Обязательное поле для имени задачи.
    description: Optional[str] = None  # Необязательное поле для описания задачи.

# Определение схемы данных для задачи с идентификатором.
class STask(STaskAdd):
    id: int  # Идентификатор задачи.

# Определение схемы данных для ответа с идентификатором задачи.
class STaskId(BaseModel):
    ok: bool = True  # Флаг успешности операции (по умолчанию True).
    task_id: int  # Идентификатор задачи.

