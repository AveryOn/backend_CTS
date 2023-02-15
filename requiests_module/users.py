##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ С ПОЛЬЗОВАТЕЛЯМИ                         #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Импорт Моделей Pydantic
from schemas_module.user import UserCreate, User

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


# Обновление данных пользователя
@user.patch('/user-update/{user_id}/', response_model=User)
def update_user(user_id: int, db: Session = Depends(sessions.get_db_USERS)) -> User:
    user = CRUD.get_user_by_id(db=db, id=user_id)
    return user


