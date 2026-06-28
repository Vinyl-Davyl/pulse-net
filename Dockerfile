# FROM = base image — official Python on Linux (alpine = small)
FROM python:3.14-slim

# WORKDIR = default directory inside container (like cd)
WORKDIR /app

# Install uv — fast Python package installer (same tool you use locally)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first (Docker layer cache — rebuilds faster when only code changes)
COPY pyproject.toml uv.lock ./

# Install dependencies into container (no dev extras for production image)
RUN uv sync --frozen --no-dev

# Copy application source
COPY app ./app
COPY main.py ./main.py
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic

# Document which port the app listens on (documentation — doesn't publish by itself)
EXPOSE 8000

# CMD = default command when container starts (one per Dockerfile)
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]