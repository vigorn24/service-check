Структура проекта

project/
├── main.py               # Основное приложение FastAPI
├── config.py             # Конфигурация (из .env)
├── models.py             # Общие Pydantic-модели
├── .env                  # Секреты (не в git!)
├── services/             # Логика взаимодействия с сервисами
│   ├── __init__.py
│   ├── redis_service.py
│   ├── rabbitmq_service.py
│   ├── mongodb_service.py
│   └── kafka_service.py
├── routers/              # Эндпоинты API
│   ├── __init__.py
│   ├── redis_router.py
│   ├── rabbitmq_router.py
│   ├── mongodb_router.py
│   └── kafka_router.py
└── requirements.txt      # Зависимости

