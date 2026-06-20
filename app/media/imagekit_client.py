from imagekitio import ImageKit
from imagekitio import NotFoundError as ImageKitNotFoundError
from imagekitio._exceptions import ImageKitError
from imagekitio.types.file_upload_response import FileUploadResponse

from app.core.config import settings


class ImageKitClient:
    def __init__(self) -> None:
        self._client = ImageKit(private_key=settings.imagekit_private_key)
        self.url_endpoint = settings.imagekit_url_endpoint

    def upload(self, file_path: str, file_name: str) -> FileUploadResponse:
        with open(file_path, "rb") as file_handle:
            return self._client.files.upload(
                file=file_handle,
                file_name=file_name,
                public_key=settings.imagekit_public_key,
                use_unique_file_name=True,
                tags=["pulse-net"],
            )

    def delete(self, file_id: str) -> None:
        self._client.files.delete(file_id)


imagekit_client = ImageKitClient()

__all__ = ["ImageKitClient", "ImageKitError", "ImageKitNotFoundError", "imagekit_client"]
