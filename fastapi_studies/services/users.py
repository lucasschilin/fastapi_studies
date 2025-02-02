from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi_studies.models.user import User
from fastapi_studies.schemas.user import UserSchema


def service_create_user(body: UserSchema, session: Session):
    user = session.scalar(
        select(User).where(
            ((User.username == body.username) | (User.email == body.email))
            & (User.deleted_at == None)
        )
    )

    if user:
        if body.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Nome de usuário não disponível.',
            )
        elif body.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Endereço de e-mail não disponível.',
            )

    user = User(
        username=body.username, email=body.email, password=body.password
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def service_get_users(session: Session):
    users = session.scalars(select(User).where(User.deleted_at == None)).all()
    return {'users': users}


def service_get_user(id: int, session: Session):
    user = session.scalar(
        select(User).where((User.id == id) & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado.',
        )

    return user


def service_update_user(id: int, body: UserSchema, session: Session):
    user = session.scalar(
        select(User).where((User.id == id) & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado.',
        )

    other_user = session.scalar(
        select(User).where(
            ((User.username == body.username) | (User.email == body.email))
            & (User.deleted_at == None)
        )
    )

    if other_user:
        if other_user.username == body.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Nome de usuário não disponível.',
            )
        elif other_user.email == body.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Endereço de e-mail não disponível.',
            )

    user.username = body.username
    user.email = body.email
    user.password = body.password

    session.commit()
    session.refresh(user)

    return user


def service_delete_user(id: int, session: Session):
    user = session.scalar(
        select(User).where((User.id == id) & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado.',
        )

    user.deleted_at = func.now()

    session.commit()

    return {'message': 'Usuário deletado.'}
