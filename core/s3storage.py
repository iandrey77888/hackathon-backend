from datetime import timedelta
import os
import uuid
from fastapi import UploadFile
from minio import Minio

from core import config

client = Minio(
    config.MINIO_URL, 
    access_key=config.MINIO_ACCESS, 
    secret_key=config.MINIO_SECRET, 
    secure=False)

def get_storage_client():
    return client
