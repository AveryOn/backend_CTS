##########################################################################################
#                      МАРШРУТ ДЛЯ ОПЕРАЦИЙ С ЧАТАМИ, СООБЩЕНИЯМИ                        #
##########################################################################################

from fastapi import APIRouter

messanger = APIRouter(
    prefix='/messanger',
    tags=["messanger"],
)

@messanger.get('/')
async def get_user():
    return {'messanger': 'hello! text!'}