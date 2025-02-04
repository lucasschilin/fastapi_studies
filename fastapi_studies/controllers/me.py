from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi_studies.models.user import User
from fastapi_studies.schemas.me import (
    UpdateMePasswordSchema,
    UpdateMeSchema,
)


def controller_get_me(session: Session):
    """Função para buscar a conta do usuário logado
    chamado pela rota GET /me/."""
    user = session.scalar(
        select(User).where((User.id == '2') & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Conta não encontrada.',
        )

    return user


def controller_update_me(body: UpdateMeSchema, session: Session):
    """Função para atualizar a conta do usuário
    chamada pela rota PUT /me/."""
    user = session.scalar(
        select(User).where((User.id == '2') & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Conta não encontrada.',
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


def controller_update_me_password(
    body: UpdateMePasswordSchema, session: Session
):
    """Função para atualizar a senha do usuário
    chamada pela rota PATCH /me/password/."""
    user = session.scalar(
        select(User).where((User.id == '2') & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Conta não encontrada.',
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


def controller_delete_me(id: int, session: Session):
    """Função para deletar o perfil do usuário
    chamada pela rota DELETE /me/."""
    user = session.scalar(
        select(User).where((User.id == '2') & (User.deleted_at == None))
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Conta não encontrada.',
        )

    user.deleted_at = func.now()

    session.commit()

    return {'message': 'Conta excluida.'}
