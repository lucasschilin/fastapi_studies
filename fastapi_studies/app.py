from http import HTTPStatus

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from fastapi_studies.database import get_session
from fastapi_studies.schemas.message import MessageSchema
from fastapi_studies.schemas.user import (
    CreateUserSchema,
    GetUserPasswordSchema,
    GetUserSchema,
    GetUsersSchema,
    UpdateUserPasswordSchema,
    UpdateUserSchema,
)
from fastapi_studies.services.users import (
    service_create_user,
    service_delete_user,
    service_get_user,
    service_get_user_password,
    service_get_users,
    service_update_user,
    service_update_user_password,
)

app = FastAPI()


@app.get('/users/', status_code=HTTPStatus.OK, response_model=GetUsersSchema)
def get_users(session: Session = Depends(get_session)):
    return service_get_users(session)


@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=GetUserSchema
)
def create_user(
    body: CreateUserSchema, session: Session = Depends(get_session)
):
    return service_create_user(body, session)


@app.get(
    '/users/{id}/', status_code=HTTPStatus.OK, response_model=GetUserSchema
)
def get_user(id: int, session: Session = Depends(get_session)):
    return service_get_user(id, session)


@app.put(
    '/users/{id}/', status_code=HTTPStatus.OK, response_model=GetUserSchema
)
def update_user(
    id: int, body: UpdateUserSchema, session: Session = Depends(get_session)
):
    return service_update_user(id, body, session)


@app.delete(
    '/users/{id}/', status_code=HTTPStatus.OK, response_model=MessageSchema
)
def delete_user(id: int, session: Session = Depends(get_session)):
    return service_delete_user(id, session)


@app.get(
    '/users/{id}/password/',
    status_code=HTTPStatus.OK,
    response_model=GetUserPasswordSchema,
)
def get_user_password(id: int, session: Session = Depends(get_session)):
    return service_get_user_password(id, session)


@app.patch(
    '/users/{id}/password/',
    status_code=HTTPStatus.OK,
    response_model=GetUserPasswordSchema,
)
def update_user_password(
    id: int,
    body: UpdateUserPasswordSchema,
    session: Session = Depends(get_session),
):
    return service_update_user_password(id, body, session)
