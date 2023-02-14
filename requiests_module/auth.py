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

auth = APIRouter(
    tags=["auth"],
)


# Создание нового пользователя
@auth.post('/registration/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(sessions.get_db_USERS)):
    return CRUD.create_user(db=db, user=user)


# Обновление данных пользователя
@auth.patch('/user_update/{user_id}/')
def update_user(user_id: int):
    return user_id

