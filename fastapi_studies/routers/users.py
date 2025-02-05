from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_studies.controllers.users_controller import (
    controller_create_user,
    controller_get_user,
    controller_get_users,
)
from fastapi_studies.database import get_session
from fastapi_studies.schemas.user import (
    CreateUserSchema,
    GetUserSchema,
    GetUsersSchema,
)

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/', status_code=HTTPStatus.OK, response_model=GetUsersSchema)
def get_users(session: Session = Depends(get_session)):
    return controller_get_users(session)


@router.get('/{id}/', status_code=HTTPStatus.OK, response_model=GetUserSchema)
def get_user(id: int, session: Session = Depends(get_session)):
    return controller_get_user(id, session)


@router.post('/', status_code=HTTPStatus.CREATED, response_model=GetUserSchema)
def create_user(
    body: CreateUserSchema, session: Session = Depends(get_session)
):
    return controller_create_user(body, session)
