from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_studies.models.user import User
from fastapi_studies.security import create_access_token, verify_password


def controller_create_auth_token(
    form_data: OAuth2PasswordRequestForm, session: Session
):
    user = session.scalar(
        select(User).where(
            (User.username == form_data.username) & (User.deleted_at == None)
        )
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}


def controller_refresh_token(current_user: User):
    new_access_token = create_access_token(data={'sub': current_user.username})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
