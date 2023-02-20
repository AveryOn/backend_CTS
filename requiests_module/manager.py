##########################################################################################
#                  МАРШРУТ ДЛЯ ОПЕРАЦИЙ МОДЕРАТОРОВ И МЕНЕДЖЕРОВ СЕРВИСА                 #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, HTTPException, Depends, Body

# Инструменты SqlAlchemy
from sqlalchemy.orm import Session

# Импорт Функций для взаимодействия с Базами Данных
from database_module import CRUD

# Импорт Моделей Pydantic
from schemas_module.user import ServicePerson
from schemas_module.product import (
    ProductCreate, 
    ProductGroupCreate, 
    ProductGroup,
    ProductCategoryCreate, 
    ProductCategory, 
    ProductChange
)
# Импорт Модуля Actions
from requiests_module.actions import sessions, auth

# Ключ доступа для сотрудников
MANAGER_KEY: str = '9dd4f7a7efd9facf9cfbd59b2411c661'

# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /manager
manager = APIRouter(
    prefix='/manager',
    tags=["manager"],
)

# ===============================>>> БЛОК ОПЕРЦИЙ ДЛЯ СОТРУДНИКА (МЕНЕДЖЕРА/МОДЕРАТОРА) <<<============================================


# Получение данных зарегестрированного СОТРУДНИКА сервиса. 
# С клиента приходит заголовок вида:  'Authorization': 'Bearer ' + access_token
@manager.get('/me/', response_model=ServicePerson)
def get_user(service_person: ServicePerson = Depends(auth.get_current_service_person)):
    return service_person


@manager.get('/get-all-service-person/', response_model=list[ServicePerson])
def get_all_service_person(db: Session = Depends(sessions.get_db_USERS)) -> list[ServicePerson]:
    return CRUD.get_all_service_person(db = db)

# ===============================>>> БЛОК ОПЕРАЦИЙ С ТОВАРАМИ <<<============================================


# Создание нового товара
@manager.post('/{manager_UUID}/create-product/')
def create_product(manager_UUID: str, product_data: dict | ProductCreate, db: Session = Depends(sessions.get_db_PRODUCTS)):
        return CRUD.create_product(db=db, creator_UUID=manager_UUID, product_data=product_data)


# ИЗМЕНЕНИЕ (редактирование) товара
@manager.put('/edit-product/{article}/')
def create_product(article: int, edit_data: ProductChange, db: Session = Depends(sessions.get_db_PRODUCTS)):
    return CRUD.edit_product(db=db, article=article, edit_data=edit_data)


# УДАЛЕНИЕ товара
@manager.delete('/delete-product/{article}/{MODERATOR_KEY}/')
# MODERATOR_KEY - приходит с клиента, как парметр пути 
def delete_product(article: int, MODERATOR_KEY: str, db: Session = Depends(sessions.get_db_PRODUCTS)):
    if MODERATOR_KEY == MANAGER_KEY:
        return CRUD.delete_product(db=db, article=article, moderator_key=MODERATOR_KEY)
    else:
        raise HTTPException(status_code=401, detail="Ключ модератора неверный!")


# ===============================>>> БЛОК ОПЕРАЦИЙ С ГРУППАМИ ТОВАРОВ <<<============================================


# Создние новой ГРУППЫ товара.  Значение поля name на клиенте должно передаваться в теле запроса в НИЖНЕМ РЕГИСТРЕ!
# Например: name: 'зима', а не: name: 'Зима'
@manager.post('/create-group-product/')
def create_group(data_group: ProductGroupCreate, db: Session = Depends(sessions.get_db_PRODUCTS)):
    try:
        return CRUD.create_group_product(db=db, data_group=data_group)
    except:
        raise HTTPException(status_code=500, detail="Не удалось создать группу товара")


# Получение ГРУППЫ товара
@manager.get('/get-group-product/{group_name}/')
def get_group(group_name: str, db: Session = Depends(sessions.get_db_PRODUCTS)):
    return CRUD.get_group_product(db=db, group_name=group_name)


# Получение СПИСКА ГРУПП товара
@manager.get('/get-all-group-product/', response_model=list[ProductGroup])
def get_all_group(db: Session = Depends(sessions.get_db_PRODUCTS)) -> list[ProductGroup]:
    return CRUD.get_all_group_product(db=db)


# ===============================>>> БЛОК ОПЕРАЦИЙ С КАТЕГОРИЯМИ ТОВАРОВ <<<============================================


# Создние новой КАТЕГОРИИ товара.  Значение поля name на клиенте должно передаваться в теле запроса в НИЖНЕМ РЕГИСТРЕ!
# Например: name: 'зима', а не: name: 'Зима'
@manager.post('/create-category-product/')
def create_category(data_category: ProductCategoryCreate, db: Session = Depends(sessions.get_db_PRODUCTS)):
    try:
        return CRUD.create_category_product(db=db, data_category=data_category)
    except:
        raise HTTPException(status_code=500, detail="Не удалось создать категорию товара")


# Получение КАТЕГОРИИ товара
@manager.get('/get-category-product/{category_name}/', response_model=ProductCategory)
def get_category(category_name: str, db: Session = Depends(sessions.get_db_PRODUCTS)) -> ProductCategory:
    return CRUD.get_catrgory_product(db=db, category_name=category_name)


# Получение СПИСКА ГРУПП товара
@manager.get('/get-all-category-product/', response_model=list[ProductCategory])
def get_all_category(db: Session = Depends(sessions.get_db_PRODUCTS)) -> list[ProductCategory]:
    return CRUD.get_all_category_product(db=db)