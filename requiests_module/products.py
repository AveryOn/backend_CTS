##########################################################################################
#                              МАРШРУТ ДЛЯ ОПЕРАЦИЙ ТОВАРАМИ                             #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, HTTPException, Depends

# Импорт Моделей Pydantic
from schemas_module.product import Product

# Импорт Функций для взаимодействия с Базами Данных
from database_module import CRUD

# Импорт Моделей Pydantic
from schemas_module.product import ProductCreate

# Импорт инструментов sqlalchemy
from sqlalchemy.orm import Session

# Импорт Модуля Actions
from requiests_module.actions import sessions

# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /products
products = APIRouter(
    prefix='/products',
    tags=["products"],
)


# Получить массив товара с БД
@products.get('/', response_model=list[Product])
async def get_products(db: Session = Depends(sessions.get_db_PRODUCTS)) -> list[Product]:
    try:
        return CRUD.get_products(db=db)
    except:
        raise HTTPException(status_code=500, detail="Не удалось получить данные товара с сервера! Попробуйте позже!")