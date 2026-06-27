import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    caption: str | None
    url: str
    file_type: str
    file_name: str
    created_at: datetime


class FeedPostRead(PostRead):
    is_owner: bool
    email: str


class FeedResponse(BaseModel):
    posts: list[FeedPostRead]
    total: int
    limit: int
    offset: int


class DeletePostResponse(BaseModel):
    success: bool
    message: str


class FeedQueryParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
