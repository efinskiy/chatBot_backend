from pydantic import BaseModel
from pydantic import Field


class AuthSchema(BaseModel):
    login: str = Field(min_length=4)
    password: str = Field(min_length=6)


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str


class BadUsernamePassword(BaseModel):
    detail: str = 'Bad username or password'


class UserCreate(BaseModel):
    login: str = Field(min_length=5)
    password: str = Field(min_length=8)
    name: str
    lastname: str


class UserRegistrationResponse(BaseModel):
    detail: str = 'User created'


class UserExists(BaseModel):
    detail: str = 'User already exists'
