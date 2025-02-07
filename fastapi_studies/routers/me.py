from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_studies.controllers.me_controller import (
    controller_delete_me,
    controller_get_me,
    controller_update_me,
    controller_update_me_password,
)
from fastapi_studies.database import get_session
from fastapi_studies.schemas.me import (
    GetMeSchema,
    UpdateMePasswordSchema,
    UpdateMeSchema,
)
from fastapi_studies.schemas.message import MessageSchema

router = APIRouter(
    prefix='/me',
    tags=['me'],
)


@router.get('/', status_code=HTTPStatus.OK, response_model=GetMeSchema)
def get_me(session: Session = Depends(get_session)):
    return controller_get_me(session)


@router.put('/', status_code=HTTPStatus.OK, response_model=GetMeSchema)
def update_me(body: UpdateMeSchema, session: Session = Depends(get_session)):
    return controller_update_me(body, session)


@router.patch(
    '/password/',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
def update_me_password(
    body: UpdateMePasswordSchema,
    session: Session = Depends(get_session),
):
    return controller_update_me_password(body, session)


@router.delete('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def delete_me(session: Session = Depends(get_session)):
    return controller_delete_me(session)
