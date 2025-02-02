from http import HTTPStatus

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from fastapi_studies.database import get_session
from fastapi_studies.schemas.message import Message
from fastapi_studies.schemas.user import UserList, UserPublic, UserSchema
from fastapi_studies.services.users import (
    service_create_user,
    service_delete_user,
    service_get_user,
    service_get_users,
    service_update_user,
)

app = FastAPI()


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(body: UserSchema, session: Session = Depends(get_session)):
    return service_create_user(body, session)


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users(session: Session = Depends(get_session)):
    return service_get_users(session)


@app.get('/users/{id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user(id: int, session: Session = Depends(get_session)):
    return service_get_user(id, session)


@app.put('/users/{id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(
    id: int, body: UserSchema, session: Session = Depends(get_session)
):
    return service_update_user(id, body, session)


@app.delete('/users/{id}/', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(id: int, session: Session = Depends(get_session)):
    return service_delete_user(id, session)
