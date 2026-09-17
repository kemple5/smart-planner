# API Contract — Smart Planner

## Схема Task 2
{
  "id": "UUID (string)",
  "title": "string",
  "description": "string",
  "status": "new | in_progress | done",
  "created_at": "ISO8601 (string)"
}

## Endpoint 1 — Task Service
POST /api/tasks
Request body (без id и created_at):
{
  "title": "string",
  "description": "string",
  "status": "new"
}
Response 201:
{
  "id": "...",
  "title": "...",
  "description": "...",
  "status": "new",
  "created_at": "2024-01-01T12:00:00Z"
}

## Endpoint 2 — Notification Service (webhook)
POST /api/webhooks/task_created
Request body — полный объект Task
Response 200:
{ "status": "received" }

## Формат сообщения вебхука
Task Service после успешного создания задачи отправляет:
POST http://localhost:8001/api/webhooks/task_created
Content-Type: application/json
Body = полный объект Task (см. схему выше)
