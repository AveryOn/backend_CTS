##########################################################################################
#                              МАРШРУТ ДЛЯ ОПЕРАЦИЙ ТОВАРАМИ                             #
##########################################################################################

from fastapi import APIRouter

products = APIRouter(
    prefix='/products',
    tags=["products"],
)

@products.get('/')
async def get_user():
    return {'products': 'hello! text!'}