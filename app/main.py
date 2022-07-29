from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from slugify import slugify
from sqladmin import Admin
from sqlalchemy.orm import Session
from typing import List

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.auth import (create_access_token, create_refresh_token,
                      get_request_user)
from app.database import get_db, engine
from app.schemas import (CategorySchema, PostSchema, CreateUserSchema,
                         Token, LoginSchema, CreatePostSchema,
                         UpdatePostSchema)
from app.models import Category, Post, User, get_random_string
from app.admin import CategoryAdmin, PostAdmin, UserAdmin
from app.hashing import Hasher
from app.send_mail import send_email

app = FastAPI()

admin = Admin(app, engine)


@app.get('/categories/', response_model=List[CategorySchema])
async def categories_list(db: Session = Depends(get_db)):
    return db.query(Category).all()


@app.get('/posts/', response_model=List[PostSchema])
async def posts_list(db: Session = Depends(get_db)):
    return db.query(Post).all()


@app.get('/posts/{slug}/', response_model=PostSchema)
async def post_details(slug, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug).first()
    if post is None:
        raise HTTPException(
            status_code=404,
            detail='Пост не найден'
        )
    return post


@app.post('/posts/', response_model=PostSchema)
async def create_post(data: CreatePostSchema,
                      db: Session = Depends(get_db),
                      user: User = Depends(get_request_user)):
    slug = slugify(data.title)
    post = Post(author_id=user.id,
                slug=slug,
                **data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.patch('/posts/{slug}/', response_model=PostSchema)
async def update_post(slug: str,
                      data: UpdatePostSchema,
                      db: Session = Depends(get_db),
                      user: User = Depends(get_request_user)):
    post = db.query(Post).filter(Post.slug == slug).first()
    if post is None:
        raise HTTPException(status_code=404,
                            detail='Пост не найден')
    if post.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail='Вы не являетесь автором')
    for key, value in data.dict().items():
        if value is not None:
            setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


@app.delete('/posts/{slug}/')
async def delete_post(slug: str,
                      db: Session = Depends(get_db),
                      user: User = Depends(get_request_user)):
    post = db.query(Post).filter(Post.slug == slug).first()
    if post is None:
        raise HTTPException(status_code=404,
                            detail='Пост не найден')
    if post.author_id != user.id:
        raise HTTPException(status_code=403,
                            detail='Вы не являетесь автором')
    db.delete(post)
    db.commit()
    return 'Пост удалён'


@app.exception_handler(RequestValidationError)
def validation_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({'detail': exc.errors()})
    )


@app.post('/register/')
def register_user(background_task: BackgroundTasks,
                  user: CreateUserSchema,
                  db: Session = Depends(get_db)):
    activation_code = get_random_string(8)
    hashed = Hasher.hash_password(user.password)
    user1 = User(**{'email': user.email, 'name': user.name})
    user1.password = hashed
    user1.activation_code = activation_code
    db.add(user1)
    db.commit()
    db.refresh(user1)
    send_email(
        background_task,
        'Активация аккаунта',
        user1.email,
        f'Для активации аккаунта перейдите по ссылке: http://localhost:8000/activate/{activation_code}/'
    )
    return user1


@app.get('/activate/{activation_code}/')
def activation(activation_code: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.activation_code == activation_code).first()
    if user:
        user.activation_code = ''
        user.is_active = True
        db.commit()
        db.refresh(user)
        return 'Ваш аккаунт успешно активирован'
    else:
        raise HTTPException(status_code=404, detail='Пользователь не найден')


@app.post('/login/', response_model=Token)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user is None:
        raise HTTPException(status_code=400,
                            detail='Неверный email')
    hashed_pass = user.password
    raw_pass = data.password
    if not Hasher.verify_password(raw_pass, hashed_pass):
        raise HTTPException(status_code=400,
                            detail='Неверный пароль')
    if not user.is_active:
        raise HTTPException(status_code=400,
                            detail='Аккаунт не активен')
    return {
        'access_token': create_access_token(str(user.id)),
        'refresh_token': create_refresh_token(str(user.id))
    }

#TODO: закончить авторизацию (логин, смена пароля и т.д.)
#TODO: сделать валидацию
#TODO: доделать админку
#TODO: CRUD
#TODO: Docker
#TODO: деплой

admin.register_model(CategoryAdmin)
admin.register_model(PostAdmin)
admin.register_model(UserAdmin)
