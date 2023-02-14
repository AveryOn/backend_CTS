##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ С ПОЛЬЗОВАТЕЛЯМИ                         #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter

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

@user.get('/')
async def get_user():
    return {'user': 'hello! text!'}