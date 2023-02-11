##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ С ПОЛЬЗОВАТЕЛЯМИ                         #
##########################################################################################

from fastapi import APIRouter

users = APIRouter(
    prefix='/users',
    tags=["users"],
)

@users.get('/')
async def get_user():
    return {'user': 'hello! text!'}