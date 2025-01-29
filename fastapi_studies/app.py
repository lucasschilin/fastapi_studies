from http import HTTPStatus

from fastapi import FastAPI

from fastapi_studies.schemas import Message, UserPublic, UserSchema, UserDB

app = FastAPI()

database = {}
database_ids = []


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    # for id, dados in database.items():
    #     if dados.username == user.username:
    #         return 'oop'
    #     elif dados.email == user.email:
    #         return 'oop'

    user_with_id = UserDB(
        id=(1 if len(database_ids) == 0 else database_ids[-1] + 1),
        **user.model_dump(),
    )

    database[user_with_id.id] = user_with_id
    database_ids.append(user_with_id.id)

    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK)
def get_users(): ...


@app.get('/users/{id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user(id: int): ...


@app.put('/users/{id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(id: int, user: UserSchema):
    return user


@app.delete('/users/{id}/', response_model=Message)
def delete_user(id: int):
    return {'message': 'User deleted'}
