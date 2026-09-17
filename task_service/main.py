import asyncio
import logging
from typing import Dict
from uuid import UUID

import httpx
from fastapi import FastAPI, HTTPException

from .models import Task, TaskCreate, build_task

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("task-service")

app = FastAPI(title="Task Service")

# In-memory storage
TASKS: Dict[UUID, Task] = {}

NOTIFICATION_WEBHOOK = "http://localhost:8001/api/webhooks/task_created"
MAX_RETRIES = 3
RETRY_DELAY = 0.5  # секунды — эмуляция "очереди сообщений в памяти"


async def send_webhook(task: Task) -> None:
    """Отправляет событие в Notification Service с ретраями.
    Не падает при ошибках — только логирует (точка отказа локально изолирована)."""
    payload = task.model_dump(mode="json")
    async with httpx.AsyncClient(timeout=3.0) as client:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = await client.post(NOTIFICATION_WEBHOOK, json=payload)
                if resp.status_code == 200:
                    log.info("Webhook delivered (attempt %s)", attempt)
                    return
                log.warning("Webhook returned %s (attempt %s)", resp.status_code, attempt)
            except httpx.HTTPError as exc:
                log.warning("Webhook error %s (attempt %s)", exc, attempt)
            await asyncio.sleep(RETRY_DELAY * attempt)

    # Финальная фиксация неудачи (здесь можно писать в файл-очередь)
    log.error("Webhook delivery FAILED for task %s after %s attempts", task.id, MAX_RETRIES)


@app.post("/api/tasks", response_model=Task, status_code=201)
async def create_task(payload: TaskCreate) -> Task:
    task = build_task(payload)
    TASKS[task.id] = task
    log.info("Task created: %s", task.id)

    # Асинхронно, не блокируя ответ клиенту
    asyncio.create_task(send_webhook(task))
    return task


@app.get("/api/tasks", response_model=list[Task])
async def list_tasks() -> list[Task]:
    return list(TASKS.values())


@app.get("/api/tasks/{task_id}", response_model=Task)
async def get_task(task_id: UUID) -> Task:
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/api/tasks/{task_id}", status_code=204)
async def delete_task(task_id: UUID) -> None:
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")
    del TASKS[task_id]