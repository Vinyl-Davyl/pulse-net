# Pulse-Net

Pulse-Net media sharing API — JWT auth, async SQLAlchemy, ImageKit-backed uploads.

## Stack

| Layer    | Technology                    |
| -------- | ----------------------------- |
| API      | FastAPI, Uvicorn              |
| Auth     | fastapi-users (JWT Bearer)    |
| ORM      | SQLAlchemy 2.x (async)        |
| Database | SQLite (default) / PostgreSQL |
| Media    | ImageKit                      |
| Client   | Streamlit (`frontend.py`)     |

## Architecture

```
frontend.py ──HTTP/JWT──► app/main.py
                              ├── auth/     register, login, users
                              ├── posts/    upload, feed, delete
                              ├── media/    ImageKit client
                              └── core/     config, database
```

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- ImageKit credentials

## Setup

```bash
uv venv && source .venv/bin/activate
uv sync --extra dev
cp .env.example .env   # fill in values
```

### Environment

| Variable               | Description                   |
| ---------------------- | ----------------------------- |
| `JWT_SECRET`           | Signing key for access tokens |
| `IMAGEKIT_PRIVATE_KEY` | ImageKit private API key      |
| `IMAGEKIT_PUBLIC_KEY`  | ImageKit public key           |
| `IMAGEKIT_URL`         | ImageKit URL endpoint         |
| `DATABASE_URL`         | Optional. Defaults to SQLite  |

## Run

```bash
# API
uv run python main.py

# Client (separate terminal)
uv run streamlit run frontend.py
```

- API: http://localhost:8000
- OpenAPI: http://localhost:8000/docs
- Client: http://localhost:8501

## API

| Method | Path                   | Auth   | Description                       |
| ------ | ---------------------- | ------ | --------------------------------- |
| POST   | `/auth/register`       | —      | Create account                    |
| POST   | `/auth/jwt/login`      | —      | Issue JWT                         |
| GET    | `/users/me`            | Bearer | Current user                      |
| POST   | `/upload`              | Bearer | Upload media + caption            |
| GET    | `/feed?limit=&offset=` | Bearer | Paginated feed                    |
| DELETE | `/posts/{post_id}`     | Bearer | Delete own post (+ ImageKit file) |

## Project layout

```
app/
├── main.py                 # Application factory
├── core/
│   ├── config.py           # pydantic-settings
│   └── database.py         # Engine, session, Base
├── auth/
│   ├── models.py           # User ORM model
│   ├── schemas.py          # User DTOs
│   ├── service.py          # UserManager
│   ├── dependencies.py     # JWT, current_user
│   └── router.py           # Auth route registration
├── posts/
│   ├── models.py           # Post ORM model
│   ├── schemas.py          # Post/feed DTOs
│   ├── service.py          # Business logic
│   └── router.py           # HTTP handlers
└── media/
    └── imagekit_client.py  # Upload / delete
```

## Database migrations

```bash
# PostgreSQL (via docker-compose)
docker compose up -d db
export DATABASE_URL=postgresql+asyncpg://pulse:pulse@localhost:5432/pulsenet

uv run alembic upgrade head
```

## Tests

```bash
uv run pytest
```

## Production notes

- Set `DATABASE_URL` to PostgreSQL and run Alembic migrations
- Disable Uvicorn `--reload`; run multiple workers behind a reverse proxy
- Rotate `JWT_SECRET`; never commit `.env`
- Replace Streamlit with your production frontend consuming the same API
