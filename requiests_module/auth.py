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
from schemas_module.user import UserCreate, User, UserLogin, ServicePersonLogin, ServicePerson

# Импорт Модуля Actions
from requiests_module.actions import sessions
from requiests_module.actions.auth import authenticate_user, authenticate_service_person, create_access_token, Token, TOKEN_KEEP_ALIVE, get_current_user

# Импорт timedelta для создания токенов доступа
from datetime import timedelta 

# Создание экземпляра маршрута
auth = APIRouter(
    tags=["auth"],
)

# Жизненный цикл токена доступа (в минутах)
TOKEN_KEEP_ALIVE = 30


# Операция пути для получения токена доступа для всех ПОЛЬЗОВАТЕЛЕЙ
@auth.post("/login-user")
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
        return [{"access_token": access_token, "token_type": "bearer"}, {"role": user.role, "user_id": user.id}]
    except:
        raise HTTPException(status_code=401, detail="Что-то пошло не так. Возможно вы ввели не верные учетные данные") 


# Операция пути для получения токена доступа для СОТРУДНИКОВ СЕРВИСА
@auth.post("/login-service-person")
async def get_access_token_service_person(form_data: ServicePersonLogin, db: Session = Depends(sessions.get_db_USERS)):
    service_person = authenticate_service_person(
        db=db,
        username=form_data.username, 
        password=form_data.password,
        UUID=form_data.UUID,
        KEY_ACCESS=form_data.KEY_ACCESS,
    )
    access_token_expires = timedelta(minutes=TOKEN_KEEP_ALIVE)
    # создание токена доступа
    access_token = create_access_token(
        data_token={"sub": str({
                "UUID": form_data.UUID, 
                "KEY_ACCESS": form_data.KEY_ACCESS, 
                "username": form_data.username,
                "role": service_person.role,
            })
        },
        expires_time=access_token_expires,
    )
    return [{"access_token": access_token, "token_type": "bearer"}, {"role": service_person.role, "UUID": service_person.UUID}]


