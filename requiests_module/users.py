##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ С ПОЛЬЗОВАТЕЛЯМИ                         #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Иснтрументы pydantic для модели обновления данных пользователя
from pydantic import BaseModel

# Импорт Моделей Pydantic
from schemas_module.user import UserCreate, User, UserChangeData, UserChangePassword

# Импорт инструментов 
from sqlalchemy.orm import Session

# Импорт модуля взаимодействия с базами данных
from database_module import CRUD

# Импорт Модуля Actions
from requiests_module.actions import sessions
from requiests_module.actions.auth import authenticate_user, create_access_token, Token, TOKEN_KEEP_ALIVE, get_current_user

# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /users
user = APIRouter(
    prefix='/user',
    tags=["user"],
)

# Создание нового пользователя
@user.post('/registration/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(sessions.get_db_USERS)):
    try:
        return CRUD.create_user(db=db, user=user)
    except:
        raise HTTPException(status_code=401, detail="Не удалось зарегистрировать нового пользователя!")


# Получение данных зарегестрированного пользователя. 
# С клиента приходит заголовок вида:  'Authorization': 'Bearer ' + access_token
@user.get('/me/', response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user


# Обновление НЕСКОЛЬКИХ данных ПОЛЬЗОВАТЕЛЯ
@user.put('/user-update/{user_id}/', response_model=User)
def update_user(user_id: int, new_data: UserChangeData, db: Session = Depends(sessions.get_db_USERS)) -> User:
    try:
        user = CRUD.get_user_by_id(db=db, id=user_id)
        return CRUD.update_user_all(db=db, new_data=new_data, user=user)
    except:
        raise HTTPException(status_code=401, detail=f"Не удалось обновить данные пользоваетеля {user.username}!")   


# Обновление пароля ПОЛЬЗОВАТЕЛЯ
@user.patch('/user-update-password/{user_id}/')
def update_user(user_id: int, new_data: UserChangePassword, db: Session = Depends(sessions.get_db_USERS)):
    try:
        CRUD.update_user_password(db=db, new_data=new_data, user_id=user_id)
        return {"status": 200}
    except:
        raise HTTPException(status_code=401, detail="Не удалось обновить пароль!")        