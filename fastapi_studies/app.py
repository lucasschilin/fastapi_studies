from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_studies.routers import auth, me, users
from fastapi_studies.schemas.message import MessageSchema

app = FastAPI(version='0.0.1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(me.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def get_root():
    return {'message': 'Olá @lucasschilin, olá Mundo! 🌎'}
