##########################################################################################
#                              МАРШРУТ ДЛЯ ОПЕРАЦИЙ ТОВАРАМИ                             #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, HTTPException, status, Depends, Query

# Импорт Моделей Pydantic
from schemas_module.product import Product

# Импорт Функций для взаимодействия с Базами Данных
from database_module import CRUD

# Импорт Моделей Pydantic
from schemas_module.product import ProductCreate, Product

# Импорт инструментов sqlalchemy
from sqlalchemy.orm import Session

# Импорт Модуля Actions
from requiests_module.actions import sessions

# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /products
products = APIRouter(
    prefix='/product',
    tags=["products"],
)


# ПОЛУЧЕНИЕ массива товаров с БД
@products.get('/', response_model=list[Product])
def get_products(db: Session = Depends(sessions.get_db_PRODUCTS)) -> list[Product]:
    try:
        return CRUD.get_products(db=db)
    except:
        raise HTTPException(status_code=500, detail="Не удалось получить данные товара с сервера! Попробуйте позже!")


# ПОЛУЧЕНИЕ конкретного товара с БД
@products.get('/get-product/{article}/', response_model=Product)
def get_product(article: int, db: Session = Depends(sessions.get_db_PRODUCTS)) -> Product:
    return CRUD.get_one_product(db=db, article=article)



# ИЗМЕНЕНИЕ рейтинга товара. (Случай, когда пользователь поставил оценку товару)
# @products.patch('/{article}/add-rating/')
# def add_rating(
#     article: int, 
#     rating: float = Query(default=..., min=1, max=5),
#     db: Session = Depends(sessions.get_db_PRODUCTS),
# ):
#     if rating >= 1:
#         product = CRUD.get_one_product(db=db, article=article)
#         if product.rating is None:
#             return CRUD.change_rating_product(db=db, article=article, rating=float(rating))
#         else:
#             product.comments
#     else:
#         raise HTTPException(status_code=400, detail="Оценка товара не определена! Операция не может быть выполнена!")


# product.comments[0].rating