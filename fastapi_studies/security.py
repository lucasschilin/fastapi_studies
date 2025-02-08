from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_studies.database import get_session
from fastapi_studies.models.user import User
from fastapi_studies.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token/')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo(Settings().TIMEZONE)) + timedelta(
        minutes=Settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        payload=to_encode,
        key=Settings().JWT_SECRET_KEY,
        algorithm=Settings().JWT_ALGORITHM,
    )

    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Invalid authentication credentials.',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token,
            secret_key=Settings().JWT_SECRET_KEY,
            algorithms=[Settings().JWT_ALGORITHM],
        )

        username: str = payload.get('sub')
        if not username:
            raise credentials_exception

    except PyJWTError:
        raise credentials_exception

    current_user = session.scalar(
        select(User).where(
            (User.username == username) & (User.deleted_at == None)
        )
    )
    if not current_user:
        raise credentials_exception

    return current_user
