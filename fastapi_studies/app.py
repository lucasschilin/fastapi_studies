from http import HTTPStatus

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from fastapi_studies.controllers.me import (
    controller_delete_me,
    controller_get_me,
    controller_update_me,
    controller_update_me_password,
)
from fastapi_studies.controllers.users_controller import (
    controller_create_user,
    controller_get_user,
    controller_get_users,
)
from fastapi_studies.database import get_session
from fastapi_studies.schemas.me import (
    GetMeSchema,
    UpdateMePasswordSchema,
    UpdateMeSchema,
)
from fastapi_studies.schemas.message import MessageSchema
from fastapi_studies.schemas.user import (
    CreateUserSchema,
    GetUserSchema,
    GetUsersSchema,
)

app = FastAPI()


# /users/ ENDPOINTS
@app.get('/users/', status_code=HTTPStatus.OK, response_model=GetUsersSchema)
def get_users(session: Session = Depends(get_session)):
    return controller_get_users(session)


@app.get(
    '/users/{id}/', status_code=HTTPStatus.OK, response_model=GetUserSchema
)
def get_user(id: int, session: Session = Depends(get_session)):
    return controller_get_user(id, session)


@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=GetUserSchema
)
def create_user(
    body: CreateUserSchema, session: Session = Depends(get_session)
):
    return controller_create_user(body, session)


# /me/ ENDPOINTS
@app.get('/me/', status_code=HTTPStatus.OK, response_model=GetMeSchema)
def get_me(session: Session = Depends(get_session)):
    return controller_get_me(session)


@app.put('/me/', status_code=HTTPStatus.OK, response_model=GetMeSchema)
def update_me(body: UpdateMeSchema, session: Session = Depends(get_session)):
    return controller_update_me(body, session)


@app.patch(
    '/me/password/',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
def update_me_password(
    body: UpdateMePasswordSchema,
    session: Session = Depends(get_session),
):
    return controller_update_me_password(body, session)


@app.delete('/me/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def delete_me(session: Session = Depends(get_session)):
    return controller_delete_me(id, session)
