from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_studies.controllers.users_controller import (
    controller_create_user,
    controller_delete_user,
    controller_get_user,
    controller_get_users,
    controller_update_user_password,
)
from fastapi_studies.database import get_session
from fastapi_studies.models.user import User
from fastapi_studies.schemas.message import MessageSchema
from fastapi_studies.schemas.user import (
    CreateUserSchema,
    GetUserSchema,
    GetUsersSchema,
    UpdateUserPasswordSchema,
)
from fastapi_studies.security import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', status_code=HTTPStatus.OK, response_model=GetUsersSchema)
def get_users(
    session: T_Session,
    current_user: T_CurrentUser,
):
    return controller_get_users(session, current_user)


@router.get('/{id}/', status_code=HTTPStatus.OK, response_model=GetUserSchema)
def get_user(id: int, session: T_Session, current_user: T_CurrentUser):
    return controller_get_user(id, session, current_user)


@router.post('/', status_code=HTTPStatus.CREATED, response_model=GetUserSchema)
def create_user(body: CreateUserSchema, session: T_Session):
    return controller_create_user(body, session)


@router.patch(
    '/{id}/password/',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
def update_user_password(
    id: int,
    body: UpdateUserPasswordSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    return controller_update_user_password(id, body, session, current_user)


@router.delete(
    '/{id}/', status_code=HTTPStatus.OK, response_model=MessageSchema
)
def delete_user(id: int, session: T_Session, current_user: T_CurrentUser):
    return controller_delete_user(id, session, current_user)
