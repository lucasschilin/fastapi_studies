from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi_studies.models.user import User
from fastapi_studies.schemas.me import (
    CreateMeSchema,
    UpdateMePasswordSchema,
    UpdateMeSchema,
)
from fastapi_studies.security import get_password_hash


def controller_get_me(session: Session, current_user: User):
    """Função para buscar a conta do usuário logado
    chamado pela rota GET /me/."""
    user = session.scalar(
        select(User).where(
            (User.id == current_user.id) & (User.deleted_at == None)
        )
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Account not found',
        )

    return user


def controller_create_me(body: CreateMeSchema, session: Session):
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
                detail='Username not available',
            )
        elif body.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='E-mail address not available',
            )

    me = User(
        username=body.username,
        email=body.email,
        password=get_password_hash(body.password),
    )

    session.add(me)
    session.commit()
    session.refresh(me)

    return me


def controller_update_me(
    body: UpdateMeSchema, session: Session, current_user: User
):
    """Função para atualizar a conta do usuário
    chamada pela rota PUT /me/."""
    user = session.scalar(
        select(User).where(
            (User.id == current_user.id) & (User.deleted_at == None)
        )
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Account not found',
        )

    other_user = session.scalar(
        select(User).where(
            ((User.username == body.username) | (User.email == body.email))
            & (User.deleted_at == None)
            & (User.id != user.id)
        )
    )

    if other_user:
        if other_user.username == body.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username not available',
            )
        elif other_user.email == body.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='E-mail address not available',
            )

    user.username = body.username
    user.email = body.email

    session.commit()
    session.refresh(user)

    return user


def controller_update_me_password(
    body: UpdateMePasswordSchema, session: Session, current_user: User
):
    """Função para atualizar a senha do usuário
    chamada pela rota PATCH /me/password/."""
    user = session.scalar(
        select(User).where(
            (User.id == current_user.id) & (User.deleted_at == None)
        )
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Account not found',
        )

    user.password = get_password_hash(body.password)

    session.commit()
    session.refresh(user)

    return {'message': 'Password changed'}


def controller_delete_me(session: Session, current_user: User):
    """Função para deletar o perfil do usuário
    chamada pela rota DELETE /me/."""
    user = session.scalar(
        select(User).where(
            (User.id == current_user.id) & (User.deleted_at == None)
        )
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Account not found',
        )

    user.deleted_by = current_user.id
    user.deleted_at = func.now()

    session.commit()

    return {'message': 'Account deleted'}
