# pulse-net

pulse-net media sharing API

## stack

| Layer    | Technology                    |
| -------- | ----------------------------- |
| API      | FastAPI, Uvicorn              |
| Auth     | fastapi-users (JWT Bearer)    |
| ORM      | SQLAlchemy 2.x (async)        |
| Database | SQLite (default) / PostgreSQL |
| Media    | ImageKit                      |
| Client   | Streamlit (`frontend.py`)     |

## setup

```bash
uv venv && source .venv/bin/activate
uv sync --extra dev
cp .env.example .env   # fill in values
```

### environment

| Variable               | Description                   |
| ---------------------- | ----------------------------- |
| `JWT_SECRET`           | Signing key for access tokens |
| `IMAGEKIT_PRIVATE_KEY` | ImageKit private API key      |
| `IMAGEKIT_PUBLIC_KEY`  | ImageKit public key           |
| `IMAGEKIT_URL`         | ImageKit URL endpoint         |
| `DATABASE_URL`         | Optional. Defaults to SQLite  |

## run

```bash
# API
uv run python main.py

# Client (separate terminal)
uv run streamlit run frontend.py
```

## API

| Method | Path                   | Auth   | Description                       |
| ------ | ---------------------- | ------ | --------------------------------- |
| POST   | `/auth/register`       | —      | Create account                    |
| POST   | `/auth/jwt/login`      | —      | Issue JWT                         |
| GET    | `/users/me`            | Bearer | Current user                      |
| POST   | `/upload`              | Bearer | Upload media + caption            |
| GET    | `/feed?limit=&offset=` | Bearer | Paginated feed                    |
| DELETE | `/posts/{post_id}`     | Bearer | Delete own post (+ ImageKit file) |

## database migrations

```bash
# PostgreSQL (via docker-compose)
docker compose up -d db
export DATABASE_URL=postgresql+asyncpg://pulse:pulse@localhost:5432/pulsenet

uv run alembic upgrade head
```

## production notes

- Set `DATABASE_URL` to PostgreSQL and run Alembic migrations
- Disable Uvicorn `--reload`; run multiple workers behind a reverse proxy
- Rotate `JWT_SECRET`; never commit `.env`
- Replace Streamlit with your production frontend consuming the same API
