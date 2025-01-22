from http import HTTPStatus

from fastapi import FastAPI, HTTPException

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
def create_user(user: UserSchema):
    try:
        return service_create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users():
    try:
        return service_get_users()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/users/{id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user(id: int):
    try:
        return service_get_user(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put('/users/{id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(id: int, user: UserSchema):
    try:
        return service_update_user(id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete('/users/{id}/', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(id: int):
    try:
        return service_delete_user(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
