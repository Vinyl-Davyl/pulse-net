import os
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

TEST_DB_PATH = Path(__file__).resolve().parent / "test.db"

os.environ.setdefault("JWT_SECRET", "test-jwt-secret-for-pytest-min-32-chars")
os.environ.setdefault("IMAGEKIT_PRIVATE_KEY", "test-private-key")
os.environ.setdefault("IMAGEKIT_PUBLIC_KEY", "test-public-key")
os.environ.setdefault("IMAGEKIT_URL", "https://ik.imagekit.io/test")
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{TEST_DB_PATH}"

if TEST_DB_PATH.exists():
    TEST_DB_PATH.unlink()


@pytest.fixture
async def client() -> AsyncClient:
    from app.core.database import create_db_and_tables
    from app.main import create_app

    await create_db_and_tables()
    app = create_app()

    async with app.router.lifespan_context(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as async_client:
            yield async_client
