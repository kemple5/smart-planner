from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    status: TaskStatus = TaskStatus.new


class Task(BaseModel):
    id: UUID
    title: str
    description: str
    status: TaskStatus
    created_at: str


def build_task(data: TaskCreate) -> Task:
    return Task(
        id=uuid4(),
        title=data.title,
        description=data.description,
        status=data.status,
        created_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )