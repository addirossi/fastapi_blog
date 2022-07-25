from decimal import Decimal
from typing import List

from fastapi import FastAPI, Depends
from sqladmin import Admin

from sqlalchemy.orm import Session

from app.admin import CategoryAdmin, PostAdmin
from app.database import get_db, engine
from app.models import Category
from app.schemas import CategorySchema, PostSchema

app = FastAPI()

admin = Admin(app, engine)


@app.get('/categories/', response_model=List[CategorySchema])
async def categories_list(db: Session = Depends(get_db)):
    return db.query(Category).all()


@app.get('/posts/', response_model=List[PostSchema])
async def categories_list(db: Session = Depends(get_db)):
    return db.query(Category).all()

admin.register_model(CategoryAdmin)
admin.register_model(PostAdmin)
