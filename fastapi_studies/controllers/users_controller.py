from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi_studies.models.user import User
from fastapi_studies.schemas.user import (
    CreateUserSchema,
    UpdateUserPasswordSchema,
)
from fastapi_studies.security import get_password_hash


def controller_get_users(session: Session):
    """Função para buscar todos os usuários
    chamada pela rota GET /users/."""
    users = session.scalars(select(User).where(User.deleted_at == None)).all()

    return {'users': users}


def controller_get_user(id: int, session: Session):
    """Função para buscar um usuário pelo id
    chamada pela rota GET /users/{id}/."""
    user = session.scalar(
        select(User).where((User.id == id) & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.',
        )

    return user


def controller_create_user(body: CreateUserSchema, session: Session):
    """Função para criar um usuário chamada pela rota POST /users/."""
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
                detail='Username not available.',
            )
        elif body.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='E-mail address not available.',
            )

    user = User(
        username=body.username,
        email=body.email,
        password=get_password_hash(body.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def controller_update_user_password(
    id: int, body: UpdateUserPasswordSchema, session: Session
):
    """Função para atualizar a senha do usuário
    chamada pela rota PATCH /me/password/."""
    user = session.scalar(
        select(User).where((User.id == id) & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.',
        )

    user.password = get_password_hash(body.password)

    session.commit()
    session.refresh(user)

    return {'message': 'Password changed.'}


def controller_delete_user(id: int, session: Session):
    """Função para deletar o perfil do usuário
    chamada pela rota DELETE /me/."""
    user = session.scalar(
        select(User).where((User.id == id) & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.',
        )

    user.deleted_at = func.now()

    session.commit()

    return {'message': 'User deleted.'}
