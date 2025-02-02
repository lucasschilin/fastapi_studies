from typing import List

from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UpdateUserSchema(BaseModel):
    username: str
    email: EmailStr


class UpdateUserPasswordSchema(BaseModel):
    password: str


class GetUserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class GetUserPasswordSchema(BaseModel):
    password: str


class GetUsersSchema(BaseModel):
    users: List[GetUserSchema]
