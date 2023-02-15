##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ С ПОЛЬЗОВАТЕЛЯМИ                         #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Импорт Моделей Pydantic
from schemas_module.user import UserCreate, User, UserLogin

# Импорт Модуля Actions
from requiests_module.actions import sessions
from requiests_module.actions.auth import authenticate_user, create_access_token, Token, TOKEN_KEEP_ALIVE, get_current_user

# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /users
user = APIRouter(
    prefix='/user',
    tags=["user"],
)

# Обновление данных пользователя
@user.patch('/user-update/{user_id}/')
def update_user(user_id: int):
    return user_id

# Получение данных зарегестрированного пользователя. 
# С клиента приходит заголовок вида:  'Authorization': 'Bearer ' + access_token
@user.get('/me/', response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user
