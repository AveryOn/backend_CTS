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
from schemas_module.user import UserCreate, User, UserLogin, ServicePersonLogin

# Импорт Модуля Actions
from requiests_module.actions import sessions
from requiests_module.actions.auth import authenticate_user, authenticate_service_person, create_access_token, Token, TOKEN_KEEP_ALIVE, get_current_user

# Импорт timedelta для создания токенов доступа
from datetime import timedelta 

# Создание экземпляра маршрута
auth = APIRouter(
    tags=["auth"],
)

# Операция пути для получения токена доступа для всех ПОЛЬЗОВАТЕЛЕЙ
@auth.post("/login-user", response_model=Token)
async def get_access_token_user(form_data: UserLogin, db: Session = Depends(sessions.get_db_USERS)):
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
            data_token={"sub": user.username},
            expires_time=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=401, detail="Что-то пошло не так. Возможно вы ввели не верные учетные данные") 


# Операция пути для получения токена доступа для СОТРУДНИКОВ СЕРВИСА
@auth.post("/login-service-person")
async def get_access_token_service_person(form_data: ServicePersonLogin, db: Session = Depends(sessions.get_db_USERS)):
    try:
        service_person = authenticate_service_person(
            db=db, 
            username=form_data.username, 
            password=form_data.password,
            UUID=form_data.UUID,
            KEY_ACCESS=form_data.KEY_ACCESS,
        )
        # Если СОТРУДНИК не прошел аутентификацию через username, password, UUID и KEY_ACCESS, то поднимается исключение
        if not service_person:
            raise HTTPException(
                status_code=401,
                detail="Не правильно введены логин или пароль!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=TOKEN_KEEP_ALIVE)
        # создание токена доступа
        access_token = create_access_token(
            data_token={"sub": str({
                    "UUID": form_data.UUID, 
                    "KEY_ACCESS": form_data.KEY_ACCESS, 
                    "username": form_data.username
                })
            },
            expires_time=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=401, detail="Что-то пошло не так. Возможно вы ввели не верные учетные данные") 


