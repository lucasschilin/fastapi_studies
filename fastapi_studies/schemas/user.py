from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class GetUserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class GetUsersSchema(BaseModel):
    users: list[GetUserSchema]
