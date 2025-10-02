from datetime import timedelta
import os
import uuid
from fastapi import UploadFile
from minio import Minio
from models.domain.hack import Files, Users
from repositories.files_repository import FilesRepository


class StorageService:
    def __init__(self, files_repo: FilesRepository, minio_client: Minio):
        self.files_repo = files_repo
        self.minio_client = minio_client

    def generate_unique_object_name(self, original_filename: str) -> str:
        # Extract file extension
        _, ext = os.path.splitext(original_filename)
        # Generate UUID
        unique_id = uuid.uuid4().hex
        # Combine UUID and extension
        return f"{unique_id}{ext}"

    def upload_file(self, current_user: Users, file: UploadFile, bucket_name: str) -> int:
        if not self.minio_client.bucket_exists(bucket_name):
            self.minio_client.make_bucket(bucket_name)

        file.file.seek(0)  # Make sure the file pointer is at start
        file_key = self.generate_unique_object_name(file.filename)
        resp = self.minio_client.put_object(
            bucket_name=bucket_name,
            object_name=file_key,
            data=file.file,
            length=-1,  # -1 allows streaming without pre-calculating size
            part_size=10*1024*1024  # 10 MB per part for multipart upload
        )
        stats = self.minio_client.stat_object(bucket_name, resp.object_name)

        new_file = Files(file_key = file_key,
            filename = file.filename,
            bucket = bucket_name,
            size = stats.size,
            checksum256 = stats.etag,
            uploader = current_user.id
            )
        self.files_repo.add_new(new_file)

        return new_file.id

    def get_file_temp(self, file_id: int, current_user: Users) -> str:
        file = self.files_repo.get_by_id(file_id)
        url = self.minio_client.presigned_get_object(
            bucket_name=file.bucket,
            object_name=file.file_key,
            expires=timedelta(hours=1),
            response_headers={
                "response-content-disposition": f'attachment; filename="{file.filename}"'
            }
        )
        return url