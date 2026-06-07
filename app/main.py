from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth.router import (
    auth_jwt_router,
    auth_register_router,
    auth_reset_password_router,
    auth_verify_router,
    users_router,
)
from app.core.database import create_db_and_tables
from app.posts.router import router as posts_router


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await create_db_and_tables()
        yield

    app = FastAPI(title="Pulse-Net", lifespan=lifespan)

    app.include_router(auth_jwt_router, prefix="/auth/jwt", tags=["auth"])
    app.include_router(auth_register_router, prefix="/auth", tags=["auth"])
    app.include_router(auth_reset_password_router, prefix="/auth", tags=["auth"])
    app.include_router(auth_verify_router, prefix="/auth", tags=["auth"])
    app.include_router(users_router, prefix="/users", tags=["users"])
    app.include_router(posts_router)

    return app


app = create_app()
