import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import current_active_user
from app.auth.models import User
from app.core.database import get_async_session
from app.posts.schemas import DeletePostResponse, FeedQueryParams, FeedResponse, PostRead
from app.posts.service import (
    MediaUploadError,
    PostForbiddenError,
    PostNotFoundError,
    PostService,
)

router = APIRouter(tags=["posts"])


@router.post("/upload", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> Post:
    try:
        return await PostService.create_post(session, user, file, caption)
    except MediaUploadError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Media upload failed",
        )


@router.get("/feed", response_model=FeedResponse)
async def get_feed(
    params: FeedQueryParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> FeedResponse:
    return await PostService.get_feed(
        session,
        user,
        limit=params.limit,
        offset=params.offset,
    )


@router.delete("/posts/{post_id}", response_model=DeletePostResponse)
async def delete_post(
    post_id: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> DeletePostResponse:
    try:
        post_uuid = uuid.UUID(post_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid post ID format",
        ) from exc

    try:
        await PostService.delete_post(session, user, post_uuid)
    except PostNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        ) from exc
    except PostForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this post",
        ) from exc

    return DeletePostResponse(success=True, message="Post deleted successfully")
