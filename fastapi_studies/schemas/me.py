from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateMeSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class GetMeSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime


class UpdateMeSchema(BaseModel):
    username: str
    email: EmailStr


class UpdateMePasswordSchema(BaseModel):
    password: str
