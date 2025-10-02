from fastapi import APIRouter, Depends, FastAPI, Form, UploadFile, File
import uuid, shutil
from pathlib import Path
from sqlalchemy.orm import Session
from api.dependencies import (
    get_buildsite_service,
    get_current_active_user,
    get_storage_service
)
from core.database import get_db
from models.domain.hack import Files
from services.storage_service import StorageService

router = APIRouter(
    prefix="/storage",
    tags=["storage"],
    #responses={404: {"description": "Not found"}},
)

@router.post("/upload/")
async def upload(nsp: str = Form(...), file: UploadFile = File(...), current_user = Depends(get_current_active_user),  storage_service: StorageService = Depends(get_storage_service)):
    res = storage_service.upload_file(current_user, file, nsp)
    return {"file_id": res}

@router.get("/fetch/")
async def get_link(file_id: int, current_user = Depends(get_current_active_user), storage_service: StorageService = Depends(get_storage_service)):
    res = storage_service.get_file_temp(file_id, current_user)
    return {"url": res}