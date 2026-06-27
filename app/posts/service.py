import os
import shutil
import tempfile
import uuid

from fastapi import UploadFile
from imagekitio import NotFoundError as ImageKitNotFoundError
from imagekitio._exceptions import ImageKitError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.auth.models import User
from app.media.imagekit_client import imagekit_client
from app.posts.models import Post
from app.posts.schemas import FeedPostRead, FeedResponse


class PostNotFoundError(Exception):
    pass


class PostForbiddenError(Exception):
    pass


class MediaUploadError(Exception):
    pass


class PostService:
    @staticmethod
    async def create_post(
        session: AsyncSession,
        user: User,
        file: UploadFile,
        caption: str,
    ) -> Post:
        temp_file_path: str | None = None

        try:
            suffix = os.path.splitext(file.filename or "")[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file_path = temp_file.name
                shutil.copyfileobj(file.file, temp_file)

            upload_result = imagekit_client.upload(
                file_path=temp_file_path,
                file_name=file.filename or "upload",
            )

            content_type = file.content_type or ""
            post = Post(
                user_id=user.id,
                caption=caption,
                url=upload_result.url or "",
                file_type="video" if content_type.startswith("video/") else "image",
                file_name=upload_result.name or file.filename or "upload",
                imagekit_file_id=upload_result.file_id,
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

        except ImageKitError as exc:
            await session.rollback()
            raise MediaUploadError("Media upload failed") from exc
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            file.file.close()

    @staticmethod
    async def get_feed(
        session: AsyncSession,
        user: User,
        limit: int,
        offset: int,
    ) -> FeedResponse:
        total_result = await session.execute(select(func.count()).select_from(Post))
        total = total_result.scalar_one()

        result = await session.execute(
            select(Post)
            .options(joinedload(Post.user))
            .order_by(Post.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        posts = result.scalars().unique().all()

        feed_posts = [
            FeedPostRead(
                id=post.id,
                user_id=post.user_id,
                caption=post.caption,
                url=post.url,
                file_type=post.file_type,
                file_name=post.file_name,
                created_at=post.created_at,
                is_owner=post.user_id == user.id,
                email=post.user.email if post.user else "Unknown",
            )
            for post in posts
        ]

        return FeedResponse(
            posts=feed_posts,
            total=total,
            limit=limit,
            offset=offset,
        )

    @staticmethod
    async def delete_post(
        session: AsyncSession,
        user: User,
        post_id: uuid.UUID,
    ) -> None:
        result = await session.execute(select(Post).where(Post.id == post_id))
        post = result.scalars().first()

        if post is None:
            raise PostNotFoundError()

        if post.user_id != user.id:
            raise PostForbiddenError()

        if post.imagekit_file_id:
            try:
                imagekit_client.delete(post.imagekit_file_id)
            except ImageKitNotFoundError:
                pass

        await session.delete(post)
        await session.commit()
