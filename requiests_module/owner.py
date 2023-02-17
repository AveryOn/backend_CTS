##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ ВЛАДЕЛЬЦА СЕРВИСА                        #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, HTTPException, Depends, Body

# Инструменты SqlAlchemy
from sqlalchemy.orm import Session

# Импорт Функций для взаимодействия с Базами Данных
from database_module import CRUD

# Импорт Моделей Pydantic
from schemas_module.user import ServicePerson, ServicePersonCreate
from schemas_module.product import (
    ProductCreate, 
    ProductGroupCreate, 
    ProductGroup, 
    ProductCategoryCreate, 
    ProductCategory,
    ProductChange,
)

# Импорт Модуля Actions
from requiests_module.actions import sessions, auth


# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /owner
owner = APIRouter(
    prefix='/owner',
    tags=["owner"],
)

# Хэш ключа владельца (ЗАМЕНИТЬ ЕГО НА ХЭШ (ДЛЯ СОЗДАНИЯ НОВОГО СОТРУДНИКА))
OWNER_KEY = '9c15a74bc8c1d16287da281402a2159d9cc1f1f18d7e26ddaba0357757b24df9'

# Для создания владельца
# SECRET_KEY: 'ce2b1cab3a9a1cc34ea66b50e2a766c68f054d81920807da4615c7bd665094e8'
# password: '$2b$12$6Oafob5Y4Pe1ZYqF.FIN8eI3u5KzOzMGKNpVcm.yhAzPw787lumXO'
# UUID: '53f48706-4fed-4251-b3ec-2d89bc386eab'


# При создании нового сотрудника (например Модератора), Владелец вводит его данные, и указывает ключ который доступен только ему
# Этот ключ служит для дополнительной безопасности, и авторизации владельца. Также он предостерегает сервис от возможного
# взлома клиента и изменения важных учетных данных

# Создание нового сотрудника
@owner.post('/create-new-person/', response_model=ServicePerson)
def create_service_person(service_person: ServicePersonCreate, db: Session = Depends(sessions.get_db_USERS)) -> ServicePerson:
    # Проверка делает сравнение хэша ключа владельца и того ключа который пришел с клиента и если они равны то блок выполняется
    if (auth.verify_password(input_password = service_person.OWNER_KEY, hashed_password = OWNER_KEY)):
        new_person = CRUD.create_service_person(db=db, service_person=service_person)
        return new_person
    else:
        raise HTTPException(status_code=408, detail='Ключ Владельца не верный!')    


# ===============================>>> БЛОК ОПЕРАЦИЙ С ТОВАРАМИ <<<============================================


# СОЗДАНИЕ нового товара
@owner.post('/{owner_UUID}/create-product/')
def create_product(owner_UUID: str, product_data: dict | ProductCreate, db: Session = Depends(sessions.get_db_PRODUCTS)):
    return CRUD.create_product(db=db, creator_UUID=owner_UUID, product_data=product_data)


# ИЗМЕНЕНИЕ (редактирование) товара
@owner.put('/edit-product/{article}/')
def create_product(article: int, edit_data: ProductChange, db: Session = Depends(sessions.get_db_PRODUCTS)):
    return CRUD.edit_product(db=db, article=article, edit_data=edit_data)


# УДАЛЕНИЕ товара
@owner.delete('/delete-product/{article}/{MODERATOR_KEY}/')
# MODERATOR_KEY - приходит с клиента, как параметр пути 
def delete_product(article: int, MODERATOR_KEY: str, db: Session = Depends(sessions.get_db_PRODUCTS)):
    if MODERATOR_KEY == OWNER_KEY:
        return CRUD.delete_product(db=db, article=article, moderator_key=MODERATOR_KEY)
    else:
        raise HTTPException(status_code=401, detail="Ключ модератора неверный!")


# ===============================>>> БЛОК ОПЕРАЦИЙ С ГРУППАМИ ТОВАРОВ <<<============================================


# Создние новой ГРУППЫ товара.  Значение поля name на клиенте должно передаваться в теле запроса в НИЖНЕМ РЕГИСТРЕ!
# Например: name: 'зима', а не: name: 'Зима'
@owner.post('/create-group-product/')
def create_group(data_group: ProductGroupCreate, db: Session = Depends(sessions.get_db_PRODUCTS)):
    try:
        return CRUD.create_group_product(db=db, data_group=data_group)
    except:
        raise HTTPException(status_code=500, detail="Не удалось создать группу товара")


# Получение ГРУППЫ товара
@owner.get('/get-group-product/{group_name}/', response_model=ProductGroup)
def get_group(group_name: str, db: Session = Depends(sessions.get_db_PRODUCTS)) -> ProductGroup:
    return CRUD.get_group_product(db=db, group_name=group_name)


# Получение СПИСКА ГРУПП товара
@owner.get('/get-all-group-product/', response_model=list[ProductGroup])
def get_all_group(db: Session = Depends(sessions.get_db_PRODUCTS)) -> list[ProductGroup]:
    return CRUD.get_all_group_product(db=db)


# ===============================>>> БЛОК ОПЕРАЦИЙ С КАТЕГОРИЯМИ ТОВАРОВ <<<============================================


# Создние новой КАТЕГОРИИ товара.  Значение поля name на клиенте должно передаваться в теле запроса в НИЖНЕМ РЕГИСТРЕ!
# Например: name: 'зима', а не: name: 'Зима'
@owner.post('/create-category-product/')
def create_category(data_category: ProductCategoryCreate, db: Session = Depends(sessions.get_db_PRODUCTS)):
    try:
        return CRUD.create_category_product(db=db, data_category=data_category)
    except:
        raise HTTPException(status_code=500, detail="Не удалось создать категорию товара")


# Получение КАТЕГОРИИ товара
@owner.get('/get-category-product/{category_name}/', response_model=ProductCategory)
def get_category(category_name: str, db: Session = Depends(sessions.get_db_PRODUCTS)) -> ProductCategory:
    return CRUD.get_catrgory_product(db=db, category_name=category_name)


# Получение СПИСКА ГРУПП товара
@owner.get('/get-all-category-product/', response_model=list[ProductCategory])
def get_all_category(db: Session = Depends(sessions.get_db_PRODUCTS)) -> list[ProductCategory]:
    return CRUD.get_all_category_product(db=db)