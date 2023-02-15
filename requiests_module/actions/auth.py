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
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
import ast

# Импорт даты для работы с токенами
from datetime import datetime, timedelta

# Импорт Функций CRUD - для взаимодействия с базами данных
from database_module import CRUD

# Импорт моделей Pydantic для аннотации типа возвращаемых данных на клиент
from schemas_module import user

# Импорт сессий баз данных из модуля actions
from requiests_module.actions import sessions

SECRET_KEY = '9c15a74bc8c1d16287da281402a2159d9cc1f1f18d7e26ddaba0357757b24df9'
MANAGER_KEY = '9dd4f7a7efd9facf9cfbd59b2411c661'
ALGORITHM = 'HS256'
TOKEN_KEEP_ALIVE = 30

# Модель для работы с ХЕШЕМ паролей (валидация и создание)
passlib = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Модель зависимости для получения токена доступа с клиента (для ПОЛЬЗОВАТЕЛЕЙ)
oauth2_user = OAuth2PasswordBearer(tokenUrl="login-user")
# Модель зависимости для получения токена доступа с клиента (для СОТРУДНИКОВ)
oauth2_service_person = OAuth2PasswordBearer(tokenUrl="login-service-person")

# Модель токена доступа для возварта на клиент
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData:
    username: str

# Функция для хеширования пароля пользователя. При его смене или создания нового пользователя
def hash_password(password: str) -> str:
    return passlib.hash(password)

# Функция верификации паролей
def verify_password(input_password: str, hashed_password: str) -> bool:
    return passlib.verify(input_password, hashed_password)


# Функция для аутентификации ПОЛЬЗОВАТЕЛЯ по логину и паролю
def authenticate_user(db: Session, login: str, password: str) -> user.User:
    try:
        user_from_db = CRUD.get_user(db=db, login=login)
        if not user_from_db:
            raise HTTPException(status_code=404, detail="Пользователя с таким логином не существует!")
        if not (verify_password(input_password=password, hashed_password=user_from_db.hashed_password)):
            raise HTTPException(status_code=407, detail="Неверный пароль!")
        return user_from_db
    except:
        # Поднимает исключение, если пользователь ввел неверные логин или пароль
        raise HTTPException(status_code=404, detail='Пользователь не найден в базе!')


# Функция для аутентификации СОТРУДНИКА по логину и паролю
def authenticate_service_person(db: Session, username: str, password: str, UUID: str, KEY_ACCESS: str) -> user.ServicePerson:
    try:
        service_person_from_db = CRUD.get_service_person(db=db, username=username)
        if not service_person_from_db:
            raise HTTPException(status_code=404, detail="Пользователя с таким логином не существует!")
        if not (verify_password(input_password=password, hashed_password=service_person_from_db.hashed_password)):
            raise HTTPException(status_code=407, detail="Неверный пароль!")
        if not service_person_from_db.UUID == UUID:
            raise HTTPException(status_code=407, detail="Неверный уникальный идентификатор!")
        if not KEY_ACCESS == MANAGER_KEY:
            raise HTTPException(status_code=407, detail="Неверный ключ доступа!")
        return service_person_from_db
    except:
        # Поднимает исключение, если пользователь ввел неверные логин или пароль
        raise HTTPException(status_code=404, detail='Пользователь не найден в базе!')


# Функция генерации токена доступа. Применяется и для Пользователей и для Сотрудников Сервиса  
def create_access_token(data_token: dict, expires_time: timedelta | None = None) -> str:
    try:
        encode_data_token = data_token.copy()
        if expires_time:
            expire = datetime.utcnow() + expires_time
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        encode_data_token.update({"exp": expire})
        return jwt.encode(encode_data_token, SECRET_KEY, ALGORITHM)
    except:
        raise HTTPException(status_code=405, detail="Ошибка в ./requiests_module/actions/auth. Ошибка при генерации токена доступа, line: 67")


# ПОЛУЧЕНИЕ ПОЛЬЗОВАТЕЛЯ ПО ТОКЕНУ ДОСТУПА
def get_current_user(token: str = Depends(oauth2_user), db: Session = Depends(sessions.get_db_USERS)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Невозможно проверить учетные данные!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = CRUD.get_user(db=db, login=username)
    if user is None:
        raise credentials_exception
    return user


# ПОЛУЧЕНИЕ СОТРУДНИКА ПО ТОКЕНУ ДОСТУПА
# Так как в обьекте payload токена в ключе "sub" можно хранить только одну строку как данные
# А для проверки сотрудников нужно учитывать несколько параметров для авторизации, 
# то ключ "sub" содержит в себе словарь в строковом формате. Исползуется бибилотека ast с методом
# ast.literal_eval который переводит структуры данных (в данном случае dict) со строки в их нативный формат
def get_current_service_person(token: str = Depends(oauth2_service_person), db: Session = Depends(sessions.get_db_USERS)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Невозможно проверить учетные данные!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # в token_data лежит словарь вида: {'UUID': str, 'KEY_ACCESS': str, 'username': str}
        token_data: dict = ast.literal_eval(payload.get("sub"))
        username: str = token_data.get("username")
        KEY_ACCESS: str = token_data.get("KEY_ACCESS")
        UUID: str = token_data.get("UUID")
        if username is None:
            raise credentials_exception
        if KEY_ACCESS != MANAGER_KEY:
            raise credentials_exception
        if UUID is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Получение сотрудника с БД
    service_person = CRUD.get_service_person(db=db, username=username)
    if not service_person.UUID == UUID:
        raise credentials_exception
    if service_person is None:
        raise credentials_exception
    return service_person

