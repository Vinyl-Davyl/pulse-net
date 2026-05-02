import uuid
from typing import Optional

from fastapi import Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from app.auth.models import User
from app.core.config import settings


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.jwt_secret
    verification_token_secret = settings.jwt_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None,
    ) -> None:
        pass

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ) -> None:
        pass

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ) -> None:
        pass
