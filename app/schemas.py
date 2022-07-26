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



class UserSchema(BaseClass):
    id: int
    email: EmailStr
    name: str
    password: str
    is_active: bool

