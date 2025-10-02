# app/api/dependencies.py
from fastapi import Depends, HTTPException, status, Header
from minio import Minio
from sqlalchemy.orm import Session
from typing import Optional, Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core import config
from core.s3storage import get_storage_client
from models.domain import hack as m

from core.database import get_db
from repositories.comments_repository import CommentsRepository
from repositories.files_repository import FilesRepository
from repositories.sitejob_repository import SitejobRepository
from services.auth_service import AuthService, oauth2_scheme
from services.buildsite_service import BuildsiteService
from repositories.user_repository import UserRepository
from repositories.buildsite_repository import BuildsiteRepository
from services.storage_service import StorageService

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repository = UserRepository(db)
    return AuthService(user_repository)

def get_buildsite_service(db: Session = Depends(get_db)) -> BuildsiteService:
    bs_repository = BuildsiteRepository(db)
    user_repository = UserRepository(db)
    comment_repository = CommentsRepository(db)
    
    sitejob_repository = SitejobRepository(db)
    return BuildsiteService(bs_repository, user_repository, comment_repository, sitejob_repository)

def get_storage_service(db: Session = Depends(get_db), client: Minio = Depends(get_storage_client)) -> StorageService:
    files_repository = FilesRepository(db)
    return StorageService(files_repository, client)

async def get_current_active_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> m.Users:
    user = auth_service.get_current_user(token)
    return user