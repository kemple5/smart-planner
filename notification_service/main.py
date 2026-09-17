import logging
from pathlib import Path

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("notification-service")

app = FastAPI(title="Notification Service")

LOG_FILE = Path("notifications.log")


class TaskEvent(BaseModel):
    id: str = Field(...)
    title: str
    description: str = ""
    status: str
    created_at: str


@app.post("/api/webhooks/task_created")
async def task_created(event: TaskEvent) -> dict:
    message = f"[NOTIFY] Новая задача: '{event.title}' (id={event.id}, status={event.status})"
    log.info(message)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(message + "\n")
    return {"status": "received"}