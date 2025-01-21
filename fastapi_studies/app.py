from http import HTTPStatus

from fastapi import FastAPI

from fastapi_studies.schemas import Message, UserSchema, UserPublic

app = FastAPI()


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    return user

@app.get("/users/")
def get_users():
    ...

@app.get("/users/{id}/", response_model=UserPublic)
def get_user(id: int):
    ...

@app.put("/users/{id}/", response_model=UserPublic)
def update_user(id: int, body: UserSchema):
    return body

@app.delete("/users/{id}/", response_model=Message)
def delete_user(id: int):
    return {"message": "User deleted"}


