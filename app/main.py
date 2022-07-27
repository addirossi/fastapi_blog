from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from typing import List
from sqladmin import Admin

from sqlalchemy.orm import Session

from app.database import get_db, engine
from app.schemas import CategorySchema, PostSchema, CreateUserSchema
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


@app.post('/register/')
def register_user(background_task: BackgroundTasks,
                  user: CreateUserSchema,
                  db: Session = Depends(get_db)):
    activation_code = get_random_string(8)
    hashed = Hasher.hash_password(user.password)
    user1 = User(**user.dict())
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


#TODO: закончить авторизацию (логин, смена пароля и т.д.)
#TODO: сделать валидацию
#TODO: доделать админку
#TODO: CRUD
#TODO: Docker
#TODO: деплой

admin.register_model(CategoryAdmin)
admin.register_model(PostAdmin)
admin.register_model(UserAdmin)
