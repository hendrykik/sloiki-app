# Słoiki app

Aplikacja do znajdywania miejsc w pociągach w Polsce, kiedy na oficjalnych stronach ich nie ma.

Zaplanowana struktura dla backendu:
backend/
├── pyproject.toml   uv.lock   Dockerfile   alembic.ini   .env.example
├── migrations/
│   ├── env.py
│   └── versions/
├── tests/
│   ├── conftest.py
│   ├── api/            services/        repositories/
└── app/
    ├── main.py          ← FastAPI(), lifespan, exception handlers
    ├── config.py        ← Settings, fail-fast
    ├── database.py      ← engine + async_sessionmaker + Base + naming convention
    ├── security.py      ← bcrypt, JWT
    ├── exceptions.py    ← bazowe wyjątki domenowe
    ├── api/
    │   ├── deps.py      ← SessionDep, CurrentUser, *ServiceDep
    │   └── v1/
    │       ├── __init__.py   ← api_router, zbiera poniższe
    │       ├── auth.py       ← POST /auth/login, /auth/register
    │       ├── events.py     ← GET /events
    │       └── health.py
    ├── models/          ← SQLAlchemy, jeden plik na tabelę
    │   ├── user.py
    │   └── event.py
    ├── schemas/         ← Pydantic, wejście/wyjście HTTP
    │   ├── auth.py
    │   └── event.py
    ├── repositories/
    │   ├── base.py      ← generyczne CRUD ← kluczowe
    │   ├── user.py
    │   └── event.py
    └── services/
        ├── auth.py
        └── event.py
