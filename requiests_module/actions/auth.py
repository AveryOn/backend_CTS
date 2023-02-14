####################################################################################################
#                               МОДУЛЬ ЗАВИСИМОСТЕЙ ДЛЯ АВТОРИЗАЦИИ                                #
####################################################################################################

# Импорт инструментов с fastapi
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Импорт инструментов pydantic 
from pydantic import BaseModel

# Инструменты SqlAlchemy
from sqlalchemy.orm import Session

# Импорт библиотек для валидации паролей и токенов
from jose import jwt, JWTError
from passlib.context import CryptContext

# Импорт даты для работы с токенами
from datetime import datetime, timedelta

# Импорт Функций CRUD - для взаимодействия с базами данных
from database_module import CRUD

# Импорт моделей Pydantic для аннотации типа возвращаемых данных на клиент
from schemas_module import user

SECRET_KEY = '9c15a74bc8c1d16287da281402a2159d9cc1f1f18d7e26ddaba0357757b24df9'
ALGORITM = 'HS256'
TOKEN_KEEP_ALIVE = 2

# Модель для работы с ХЕШЕМ паролей (валидация и создание)
passlib = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Модель зависимости для получения токена доступа с клиента
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Модель токена доступа для возварта на клиент
class Token(BaseModel):
    access_token: str
    token_type: str


# Функция для хеширования пароля пользователя. При его смене или создания нового пользователя
def hash_password(password: str) -> str:
    return passlib.hash(password)

# Функция верификации паролей
def verify_password(input_password: str, hashed_password: str) -> bool:
    return passlib.verify(input_password, hashed_password)


# Функция для аутентификации ПОЛЬЗОВАТЕЛЯ по логину и паролю
def authenticate_user(db: Session, login: str, password: str) -> user.User:
    user_from_db = CRUD.get_user(db=db, login=login)
    if not user_from_db:
        raise HTTPException(status_code=404, detail="Пользователя с таким логином не существует!")
    if not (verify_password(input_password=password, hashed_password=user_from_db.hashed_password)):
        raise HTTPException(status_code=407, detail="Неверный пароль!")
    return user_from_db