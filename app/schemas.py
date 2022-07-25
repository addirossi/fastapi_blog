from pydantic import BaseModel


class CategorySchema(BaseModel):
    title: str
    slug: str

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    id: int
    title: str
    slug: str
    text: str
    category: CategorySchema
