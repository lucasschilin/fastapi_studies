from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fastapi_studies.models.user import User
from fastapi_studies.schemas.user import UserDB, UserSchema
from fastapi_studies.settings import Settings

database = {}
database_ids = []


def service_create_user(user: UserSchema):
    engine = create_engine(Settings().DATABASE_URL)

    with Session(engine) as session:
        user_db = session.scalar(
            select(User).where(
                ((User.username == user.username) | (User.email == user.email))
                & (User.deleted_at == None)
            )
        )

        if user_db:
            if user.username == user_db.username:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail='Usuário não disponível.',
                )
            elif user.email == user_db.email:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail='Endereço de e-mail não disponível.',
                )

        user_db = User(
            username=user.username, email=user.email, password=user.password
        )

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

    return user_db


def service_get_users():
    return {'users': []}


def service_get_user(id: int):
    engine = create_engine(Settings().DATABASE_URL)

    with Session(engine) as session:
        user_db = session.scalar(
            select(User).where((User.id == id) & (User.deleted_at == None))
        )

        if not user_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Usuário não encontrado.',
            )

    return user_db


def service_update_user(id: int, user: UserSchema):
    if id not in database:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado.',
        )

    user_with_id = UserDB(
        id=id,
        **user.model_dump(),
    )
    database[id] = user_with_id

    return user_with_id


def service_delete_user(id: int):
    if id not in database:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado.',
        )

    database.pop(id, None)

    return {'message': 'Usuário deletado.'}
