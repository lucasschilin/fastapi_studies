from http import HTTPStatus

from fastapi import FastAPI

from fastapi_studies.routers import auth, me, users
from fastapi_studies.schemas.message import MessageSchema

app = FastAPI()

app.include_router(me.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def get_root():
    return {'message': 'Olá @lucasschilin, olá Mundo! 🌎'}
