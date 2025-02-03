from http import HTTPStatus

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from fastapi_studies.controllers.profile_controller import (
    controller_delete_profile,
    controller_get_profile,
    controller_update_profile,
    controller_update_profile_password,
)
from fastapi_studies.controllers.users_controller import (
    controller_create_user,
    controller_get_user,
    controller_get_users,
)
from fastapi_studies.database import get_session
from fastapi_studies.schemas.message import MessageSchema
from fastapi_studies.schemas.profile import (
    GetProfileSchema,
    UpdateProfilePasswordSchema,
    UpdateProfileSchema,
)
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


# /profile/ ENDPOINTS
@app.get(
    '/profile/', status_code=HTTPStatus.OK, response_model=GetProfileSchema
)
def get_profile(session: Session = Depends(get_session)):
    return controller_get_profile(session)


@app.put(
    '/profile/', status_code=HTTPStatus.OK, response_model=GetProfileSchema
)
def update_profile(
    body: UpdateProfileSchema, session: Session = Depends(get_session)
):
    return controller_update_profile(body, session)


@app.patch(
    '/profile/password/',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
def update_profile_password(
    body: UpdateProfilePasswordSchema,
    session: Session = Depends(get_session),
):
    return controller_update_profile_password(body, session)


@app.delete(
    '/profile/', status_code=HTTPStatus.OK, response_model=MessageSchema
)
def delete_profile(session: Session = Depends(get_session)):
    return controller_delete_profile(id, session)
