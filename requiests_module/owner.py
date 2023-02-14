##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ ВЛАДЕЛЬЦА СЕРВИСА                        #
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

owner = APIRouter(
    prefix='/owner',
    tags=["owner"],
)

# password: '$2b$12$6Oafob5Y4Pe1ZYqF.FIN8eI3u5KzOzMGKNpVcm.yhAzPw787lumXO'
# UUID: '53f48706-4fed-4251-b3ec-2d89bc386eab'


# Создание нового сотрудника
@owner.post('/create-new-person/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(sessions.get_db_USERS)):
    return CRUD.create_user(db=db, user=user)

@owner.get('/create-new-person/')
def get_some():
    return '200 ok'
