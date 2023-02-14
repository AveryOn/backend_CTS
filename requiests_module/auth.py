##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ С АУТЕНТИФИКАЦИЕЙ                        #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Инструменты SqlAlchemy
from sqlalchemy.orm import Session

# Импорт Функций для взаимодействия с Базами Данных
from database_module import CRUD

# Импорт Моделей Pydantic
from schemas_module.user import UserCreate, User, UserLogin

# Импорт Модуля Actions
from requiests_module.actions import sessions
from requiests_module.actions.auth import authenticate_user, create_access_token, Token, TOKEN_KEEP_ALIVE
auth = APIRouter(
    tags=["auth"],
)

# Операция пути для получения токена доступа для всех ПОЛЬЗОВАТЕЛЕЙ
@auth.post("/token", response_model=Token)
async def get_access_token(form_data: UserLogin, db: Session = Depends(sessions.get_db_USERS)):
    try:
        user = authenticate_user(db=db, login=form_data.username, password=form_data.password)
        # Если пользователь не прошел аутентификацию через логин и пароль, то поднимается исключение
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Не правильно введены логин или пароль!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=TOKEN_KEEP_ALIVE)
        access_token = create_access_token(
            data_token={
                "sub": {
                    "username": user.username,
                    "role": user.role,
                }
            },
            expires_time=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=401, detail="Не удалось пройти авторизацию, попробуйте позже...") 


# Создание нового пользователя
@auth.post('/registration/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(sessions.get_db_USERS)):
    return CRUD.create_user(db=db, user=user)


#               !! ТЕСТОВЫЕ ПУТИ !!
from datetime import timedelta

# !!ПЕРЕНЕСТИ В USERS РОУТЕР !!
@auth.get('/get-user/{login}/{password}/', response_model=User)
def get_user(login: str, password: str, db: Session = Depends(sessions.get_db_USERS)):
    user_from_db = authenticate_user(db=db, login=login, password=password)
    return user_from_db

# !! TEST !!
@auth.get('/get-user/')
def get_user():
    token = create_access_token(data_token={"sub": {"username": 'tomas123'}})
    return token

