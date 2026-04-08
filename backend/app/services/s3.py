"""S3 storage service for resume file management."""

import logging
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from app.core.config import settings

logger = logging.getLogger(__name__)


class S3Service:
    """Service for managing file uploads to S3 or local fallback storage."""

    def __init__(self) -> None:
        """Initialize S3 client using application settings."""
        self._client = None
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            client_kwargs: dict = {
                "service_name": "s3",
                "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
                "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
                "region_name": settings.AWS_REGION,
            }
            if settings.S3_ENDPOINT_URL:
                client_kwargs["endpoint_url"] = settings.S3_ENDPOINT_URL
            self._client = boto3.client(**client_kwargs)
        else:
            logger.warning(
                "S3 credentials not configured — using local file storage fallback."
            )

    @property
    def _local_storage_dir(self) -> Path:
        """Return the local fallback storage directory."""
        path = Path("local_uploads")
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _local_path_for_key(self, key: str) -> Path:
        """Convert an S3 key to a local file path."""
        return self._local_storage_dir / key.replace("/", "_")

    def upload_file(self, file_content: bytes, key: str) -> str:
        """Upload a file to S3 or local fallback storage.

        Args:
            file_content: Raw file bytes to upload.
            key: The S3 object key (or local filename).

        Returns:
            The storage key/path where the file was saved.
        """
        if self._client:
            try:
                self._client.put_object(
                    Bucket=settings.S3_BUCKET,
                    Key=key,
                    Body=file_content,
                )
                logger.info("Uploaded file to S3: %s", key)
                return key
            except ClientError:
                logger.exception("Failed to upload file to S3: %s", key)
                raise
        else:
            local_path = self._local_path_for_key(key)
            local_path.write_bytes(file_content)
            logger.info("Saved file locally: %s", local_path)
            return str(local_path)

    def get_presigned_url(self, key: str, expiration: int = 3600) -> str:
        """Generate a presigned URL for downloading a file from S3.

        Args:
            key: The S3 object key.
            expiration: URL expiration time in seconds (default 1 hour).

        Returns:
            Presigned URL string, or local file path if S3 is not configured.
        """
        if self._client:
            try:
                url: str = self._client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": settings.S3_BUCKET, "Key": key},
                    ExpiresIn=expiration,
                )
                return url
            except ClientError:
                logger.exception("Failed to generate presigned URL for: %s", key)
                raise
        else:
            local_path = self._local_path_for_key(key)
            return f"file://{local_path.resolve()}"

    def delete_file(self, key: str) -> bool:
        """Delete a file from S3 or local storage.

        Args:
            key: The S3 object key or local file path.

        Returns:
            True if deletion succeeded, False otherwise.
        """
        if self._client:
            try:
                self._client.delete_object(
                    Bucket=settings.S3_BUCKET,
                    Key=key,
                )
                logger.info("Deleted file from S3: %s", key)
                return True
            except ClientError:
                logger.exception("Failed to delete file from S3: %s", key)
                return False
        else:
            local_path = self._local_path_for_key(key)
            if local_path.exists():
                local_path.unlink()
                logger.info("Deleted local file: %s", local_path)
                return True
            logger.warning("Local file not found for deletion: %s", local_path)
            return False


s3_service = S3Service()
