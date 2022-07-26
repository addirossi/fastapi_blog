from fastapi import FastAPI
from fastapi import Depends
from typing import List
from sqladmin import Admin

from sqlalchemy.orm import Session

from app.database import get_db, engine
from app.schemas import CategorySchema, PostSchema, UserSchema
from app.models import Category, Post, User
from app.admin import CategoryAdmin, PostAdmin, UserAdmin


app = FastAPI()

admin = Admin(app, engine)


@app.get('/categories/', response_model=List[CategorySchema])
async def categories_list(db: Session = Depends(get_db)):
    return db.query(Category).all()


@app.get('/posts/', response_model=List[PostSchema])
async def posts_list(db: Session = Depends(get_db)):
    return db.query(Post).all()


@app.post('/register/')
def register_user(user: UserSchema, db: Session = Depends(get_db)):
    user1 = User(**user.dict())
    db.add(user1)
    db.commit()
    db.refresh(user1)
    return user1


admin.register_model(CategoryAdmin)
admin.register_model(PostAdmin)
admin.register_model(UserAdmin)