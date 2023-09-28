from pydantic import BaseModel, Field, EmailStr
from typing import Union, List, Tuple

from .generic import Base


class TokenSchema(Base):
    access_token: str
    refresh_token: str


class UserAuth(Base):
    username: str = Field(..., description="username")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    email: EmailStr


class User(Base):
    username: str
    email: EmailStr

class TokenPayload(Base):
    sub: str = None
    exp: int = None


class LoginCreds(Base):
    username: str
    password: str

class APIKey(Base):
    api_key: str