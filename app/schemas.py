from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseClass(BaseModel):
    class Config:
        orm_mode = True


class CategorySchema(BaseClass):
    title: str
    slug: str


class PostSchema(BaseClass):
    id: int
    title: str
    slug: str
    text: str
    category: CategorySchema


class CreatePostSchema(BaseClass):
    title: str
    text: str
    category: CategorySchema


class UpdatePostSchema(BaseClass):
    title: Optional[str]
    text: Optional[str]


class CreateUserSchema(BaseClass):
    email: EmailStr
    name: str
    password: str


class UserSchema(BaseClass):
    id: int
    email: EmailStr
    name: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    refresh_token: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenPayload(BaseModel):
    sub: str
    exp: int
