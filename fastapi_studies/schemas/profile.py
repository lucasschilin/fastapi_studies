from datetime import datetime

from pydantic import BaseModel, EmailStr


class GetProfileSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime


class UpdateProfileSchema(BaseModel):
    username: str
    email: EmailStr


class UpdateProfilePasswordSchema(BaseModel):
    password: str
