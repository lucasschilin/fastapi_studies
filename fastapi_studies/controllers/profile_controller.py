from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi_studies.models.user import User
from fastapi_studies.schemas.profile import (
    UpdateProfilePasswordSchema,
    UpdateProfileSchema,
)


def controller_get_profile(session: Session):
    """Função para buscar o perfil do usuário"""
    user = session.scalar(
        select(User).where((User.id == '2') & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Perfil não encontrado.',
        )

    return user


def controller_update_profile(body: UpdateProfileSchema, session: Session):
    """Função para atualizar o perfil do usuário
    chamada pela rota PUT /users/{id}/."""
    user = session.scalar(
        select(User).where((User.id == '2') & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Perfil não encontrado.',
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
                detail='Nome de usuário não disponível.',
            )
        elif other_user.email == body.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Endereço de e-mail não disponível.',
            )

    user.username = body.username
    user.email = body.email

    session.commit()
    session.refresh(user)

    return user


def controller_update_profile_password(
    body: UpdateProfilePasswordSchema, session: Session
):
    """Função para atualizar a senha do usuário
    chamada pela rota PATCH /profile/password/."""
    user = session.scalar(
        select(User).where((User.id == '2') & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Perfil não encontrado.',
        )

    if user.password == body.password:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Senha igual a atual.',
        )

    user.password = body.password

    session.commit()
    session.refresh(user)

    return {'message': 'Senha alterada.'}


def controller_delete_profile(id: int, session: Session):
    """Função para deletar o perfil do usuário"""
    user = session.scalar(
        select(User).where((User.id == '2') & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Perfil não encontrado.',
        )

    user.deleted_at = func.now()

    session.commit()

    return {'message': 'Perfil deletado.'}
