##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ С ПОЛЬЗОВАТЕЛЯМИ                         #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Импорт Моделей Pydantic
from schemas_module.user import UserCreate, User, UserChangeData, UserChangePassword

# Импорт инструментов 
from sqlalchemy.orm import Session

# Импорт модуля взаимодействия с базами данных
from database_module import CRUD

# Импорт Модуля Actions
from requiests_module.actions import sessions
from requiests_module.actions.auth import get_current_user

# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /users
user = APIRouter(
    prefix='/user',
    tags=["user"],
)

# Получение данных о коризне ПОЛЬЗОВАТЕЛЯ
@user.get('/{user_id}/cart/')
def get_cart_user(user_id: int, db: Session = Depends(sessions.get_db_USERS)):
    try:
        return CRUD.get_user_cart(db=db, user_id=user_id)
    except:
        raise HTTPException(status_code=400, detail="Не удалось получить доступ к корзине пользователя") 


# Создание нового ПОЛЬЗОВАТЕЛЯ
@user.post('/registration/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(sessions.get_db_USERS)):
    try:
        return CRUD.create_user(db=db, user=user)
    except:
        raise HTTPException(status_code=401, detail="Не удалось зарегистрировать нового пользователя!")


# Получение данных зарегестрированного ПОЛЬЗОВАТЕЛЯ. 
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
def update_user_password(user_id: int, new_data: UserChangePassword, db: Session = Depends(sessions.get_db_USERS)) -> dict:
    try:
        CRUD.update_user_password(db=db, new_data=new_data, user_id=user_id)
        return {"response_status": 'Successful!'}
    except:
        raise HTTPException(status_code=401, detail="Не удалось обновить пароль!")


# Удаление ПОЛЬЗОВАТЕЛЯ
@user.delete('/user-delete/{user_id}')
def delete_user(user_id: int, db: Session = Depends(sessions.get_db_USERS)) -> dict:
    try:
        CRUD.delete_user(db=db, user_id=user_id)
        return {"response_status": 'Successful!'}
    except:
        raise HTTPException(status_code=400, detail="Не удалось удалить пользователя из базы")