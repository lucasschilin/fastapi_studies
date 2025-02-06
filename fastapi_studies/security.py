from zoneinfo import ZoneInfo
from pwdlib import PasswordHash
from datetime import datetime, timedelta

from jwt import encode

from fastapi_studies.settings import Settings

pwd_context = PasswordHash.recommended()


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
