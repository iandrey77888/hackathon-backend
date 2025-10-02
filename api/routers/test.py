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
    prefix="/test",
    tags=["test"],
    #responses={404: {"description": "Not found"}},
)

@router.post("/token", response_model=schm.LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    return schm.LoginResponse(**(auth_service.login_for_access_token(form_data)))

@router.post("/json-protected", response_model=schm.ProtectedResponse)
@AuthService.dec_check_roles(roles=[ERole.CONTRACTOR, ERole.FOREMAN])
async def json_protected_route(
    data: schm.TestRequest,
    current_user: m.Users = Depends(get_current_active_user)
):
    return schm.ProtectedResponse(
        message=f"Все ок, пользователь {current_user} авторизован"
        , your_data = data.dict()
    )