from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_studies.controllers.me_controller import (
    controller_create_me,
    controller_delete_me,
    controller_get_me,
    controller_update_me,
    controller_update_me_password,
)
from fastapi_studies.database import get_session
from fastapi_studies.models.user import User
from fastapi_studies.schemas.me import (
    CreateMeSchema,
    GetMeSchema,
    UpdateMePasswordSchema,
    UpdateMeSchema,
)
from fastapi_studies.schemas.message import MessageSchema
from fastapi_studies.security import get_current_user

router = APIRouter(
    prefix='/me',
    tags=['Me'],
)

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', status_code=HTTPStatus.OK, response_model=GetMeSchema)
def get_me(session: T_Session, current_user: T_CurrentUser):
    return controller_get_me(session, current_user)


@router.post('/', status_code=HTTPStatus.CREATED, response_model=GetMeSchema)
def create_me(body: CreateMeSchema, session: T_Session):
    return controller_create_me(body, session)


@router.put('/', status_code=HTTPStatus.OK, response_model=GetMeSchema)
def update_me(
    body: UpdateMeSchema, session: T_Session, current_user: T_CurrentUser
):
    return controller_update_me(body, session, current_user)


@router.patch(
    '/password/', status_code=HTTPStatus.OK, response_model=MessageSchema
)
def update_me_password(
    body: UpdateMePasswordSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    return controller_update_me_password(body, session, current_user)


@router.delete('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def delete_me(session: T_Session, current_user: T_CurrentUser):
    return controller_delete_me(session, current_user)
