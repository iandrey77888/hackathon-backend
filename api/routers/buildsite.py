from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
import models.schemas.hack as schm
from core.logger import logger
from models.domain import hack as m
from services.auth_service import AuthService, ERole
from api.dependencies import (
    get_buildsite_service,
    get_current_active_user
)
from models.schemas.hack import BuildsitePaginationRequest, BuildsiteListResponse, BuildsiteResponse, BuildsiteExtendedResponse, CommentCreationRequest, CommentCreationResponce
from services.buildsite_service import BuildsiteService

router = APIRouter(
    prefix="/buildsite",
    tags=["buildsite"],
    #responses={404: {"description": "Not found"}},
)

@router.get("/getAvailableObjects", response_model=BuildsiteListResponse)
async def get_available_objects(
    request: BuildsitePaginationRequest = Depends(),
    current_user = Depends(get_current_active_user),
    buildsite_service: BuildsiteService = Depends(get_buildsite_service)
):
    return buildsite_service.get_available_objects(current_user, request)

@router.get("/getObjectData", response_model = BuildsiteResponse | BuildsiteExtendedResponse, description="Подробная инфомрация об одном объекте")
async def get_buildsite_by_id(
    buildsite_id: int = Query(..., description="ID объекта", example=123, alias="id"),
    need_details: bool = Query(False, description="Опеределяет необходимость вернуть детальную информацию по объекту (комментарии и прочее)", examples=["true", "false"], alias="details"),
    current_user: m.Users = Depends(get_current_active_user),
    buildsite_service: BuildsiteService = Depends(get_buildsite_service)
):
    buildsite = buildsite_service.get_buildsite_by_id(buildsite_id, current_user, need_details)
    return buildsite

#CommentCreationRequest
@router.post("/createComment", response_model=CommentCreationResponce)
async def get_available_objects(
    request: CommentCreationRequest,
    current_user = Depends(get_current_active_user),
    buildsite_service: BuildsiteService = Depends(get_buildsite_service)
):
    return buildsite_service.process_comment_creation(current_user, request)