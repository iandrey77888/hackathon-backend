from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import models.schemas.hack as schm
from core.logger import logger
from models.domain import hack as m
from services.auth_service import AuthService, ERole, oauth2_scheme
from api.dependencies import (
    get_auth_service,
    get_current_active_user
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    #responses={404: {"description": "Not found"}},
)

@router.post("/token", response_model=schm.LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    return schm.LoginResponse(**(auth_service.login_for_access_token(form_data)))

@router.get("/me", response_model=schm.UserResponse, description="Получение информации по текущему пользователю")
async def get_current_user(
    current_user: m.Users = Depends(get_current_active_user)
):
    return schm.UserResponse.model_validate(current_user)
