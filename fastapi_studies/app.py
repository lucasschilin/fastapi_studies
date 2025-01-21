from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fastapi_studies.schemas.message import Message
from fastapi_studies.schemas.user import UserList, UserPublic, UserSchema
from fastapi_studies.services.users import (
    controller_create_user,
    controller_delete_user,
    controller_get_user,
    controller_get_users,
    controller_update_user,
)

app = FastAPI()


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    try:
        return controller_create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users():
    return controller_get_users()
    # try:
    # except ValueError as e:
    #     raise HTTPException(status_code=400, detail=str(e))


@app.get('/users/{id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user(id: int):
    try:
        return controller_get_user(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put('/users/{id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(id: int, user: UserSchema):
    try:
        return controller_update_user(id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete('/users/{id}/', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(id: int):
    try:
        return controller_delete_user(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
