##########################################################################################
#                              МАРШРУТ ДЛЯ ОПЕРАЦИЙ ТОВАРАМИ                             #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, HTTPException, Depends

# Импорт Моделей Pydantic
from schemas_module.user import ServicePerson, ServicePersonCreate
from schemas_module.product import ProductCreate

# Импорт Функций для взаимодействия с Базами Данных
from database_module import CRUD

# Импорт Моделей Pydantic
from schemas_module.user import ServicePerson, ServicePersonCreate
from schemas_module.product import ProductCreate

# Импорт инструментов sqlalchemy
from sqlalchemy.orm import Session

# Импорт Модуля Actions
from requiests_module.actions import sessions, auth

# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /products
products = APIRouter(
    prefix='/products',
    tags=["products"],
)


# Получить массив товара с БД
@products.get('/')
async def get_products(db: Session = Depends(sessions.get_db_PRODUCTS)):
    return CRUD.get_products(db=db)