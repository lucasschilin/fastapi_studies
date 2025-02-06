from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_studies.controllers.auth_controller import (
    controller_create_auth_token,
)
from fastapi_studies.database import get_session

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/token/')
def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    return controller_create_auth_token(form_data, session)
