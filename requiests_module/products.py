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
from schemas_module.comment import Comment

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


# ПОЛУЧЕНИЕ СПИСКА комментариев конкретного товара. Индексация товара по артикулу
@products.get('/get-comments/{article}', response_model=list[Comment])
def get_comments(article: int, db: Session = Depends(sessions.get_db_PRODUCTS)) -> list[Comment]:
    return CRUD.get_all_comments(db=db, article=article)


# УДАЛЕНИЕ комментария
@products.delete('/{article}/delete-comment/{comment_id}/')
def delete_comment(article: int, comment_id: int, db: Session = Depends(sessions.get_db_PRODUCTS)):
    return CRUD.delete_comment(db=db, comment_id=comment_id, article=article)