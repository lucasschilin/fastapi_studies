from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_studies.controllers.auth_controller import (
    controller_create_auth_token,
    controller_refresh_token,
)
from fastapi_studies.database import get_session
from fastapi_studies.models.user import User
from fastapi_studies.schemas.token import TokenSchema
from fastapi_studies.security import get_current_user

router = APIRouter(prefix='/auth', tags=['Auth'])

T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/token/', response_model=TokenSchema)
def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    return controller_create_auth_token(form_data, session)


@router.post('/refresh-token/', response_model=TokenSchema)
def refresh_token(current_user: T_CurrentUser):
    return controller_refresh_token(current_user)
