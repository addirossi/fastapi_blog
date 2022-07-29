import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.hashing import Hasher
from app.models import User
from app.schemas import UserSchema, TokenPayload

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_LIFETIME = int(os.getenv('ACCESS_TOKEN_LIFETIME'))
REFRESH_TOKEN_LIFETIME = int(os.getenv('REFRESH_TOKEN_LIFETIME'))


def create_access_token(subject: str) -> str:
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    payload = {"exp": expiration_time, "sub": subject}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str) -> str:
    expiration_time = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_LIFETIME)
    payload = {"exp": expiration_time, "sub": subject}
    encoded_jwt = jwt.encode(payload, REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


reusable_oauth = OAuth2PasswordBearer(
    tokenUrl='/login/',
    scheme_name='JWT'
)


def get_request_user(token: str = Depends(reusable_oauth), db: Session = Depends(get_db)) -> UserSchema:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=401,
                                detail='Токен истек',
                                headers={"WWW-Authenticate": "Bearer"})
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail='Неверный токен',
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = db.get(User, token_data.sub)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='Пользователь не найден'
        )
    data = {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'is_active': user.is_active
    }
    return UserSchema(**data)
