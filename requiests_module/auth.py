##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ С АУТЕНТИФИКАЦИЕЙ                        #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, Depends

# Инструменты SqlAlchemy
from sqlalchemy.orm import Session

# Импорт Функций для взаимодействия с Базами Данных
from database_module import CRUD

# Импорт Моделей Pydantic
from schemas_module.user import UserCreate, User

# Импорт Модуля Actions
from requiests_module.actions import sessions
from requiests_module.actions.auth import authenticate_user
auth = APIRouter(
    tags=["auth"],
)


# Создание нового пользователя
@auth.post('/registration/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(sessions.get_db_USERS)):
    return CRUD.create_user(db=db, user=user)


# !!ПЕРЕНЕСТИ В USERS РОУТЕР !!
@auth.get('/get-user/{login}/{password}/', response_model=User)
def get_user(login: str, password: str, db: Session = Depends(sessions.get_db_USERS)):
    user_from_db = authenticate_user(db=db, login=login, password=password)
    return user_from_db

