# Smart Planner — «Умный планировщик задач»

Прототип сервиса для управления задачами с асинхронными уведомлениями.
Лабораторная работа по МДК 02.02 — командная разработка, contract-first, интеграция через PR.

## Архитектура

Система состоит из двух независимых микросервисов:

| Сервис | Порт | Ответственность |
|--------|------|-----------------|
| **Task Service** | 8000 | CRUD задач: создание, чтение, удаление |
| **Notification Service** | 8001 | Приём вебхука о создании задачи, запись уведомления в лог |

Взаимодействие — **асинхронное**, через HTTP-вебхук:
после создания задачи Task Service отправляет POST-запрос в Notification Service.

## Стек

- Python 3.10+
- FastAPI + Uvicorn
- httpx (для исходящих вебхуков)
- pytest + pytest-asyncio (тесты)
- Pydantic (валидация данных)

## Структура проекта
smart-planner/
├── API_CONTRACT.md # Единый контракт API (источник истины)
├── README.md # Этот файл
├── requirements.txt # Зависимости Python
├── task_service/
│ ├── init.py
│ ├── main.py # FastAPI-приложение Task Service
│ └── models.py # Pydantic-модели Task и TaskCreate
├── notification_service/
│ ├── init.py
│ └── main.py # FastAPI-приложение Notification Service
└── tests/
├── init.py
├── test_task_service.py # Юнит-тесты Task Service
├── test_notification_service.py # Юнит-тесты Notification Service
└── test_integration.py # E2E-тест
