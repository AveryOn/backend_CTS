##########################################################################################
#                  МАРШРУТ ДЛЯ ОПЕРАЦИЙ МОДЕРАТОРОВ И МЕНЕДЖЕРОВ СЕРВИСА                 #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, HTTPException, Depends

# Инструменты SqlAlchemy
from sqlalchemy.orm import Session

# Импорт Функций для взаимодействия с Базами Данных
from database_module import CRUD

# Импорт Моделей Pydantic
from schemas_module.user import ServicePerson
from schemas_module.product import ProductCreate, Product

# Импорт Модуля Actions
from requiests_module.actions import sessions, auth


# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /manager
manager = APIRouter(
    prefix='/manager',
    tags=["manager"],
)

# Получение данных зарегестрированного СОТРУДНИКА сервиса. 
# С клиента приходит заголовок вида:  'Authorization': 'Bearer ' + access_token
@manager.get('/me/', response_model=ServicePerson)
def get_user(service_person: ServicePerson = Depends(auth.get_current_service_person)):
    return service_person


# Создание нового товара
@manager.post('/{manager_UUID}/create-product/')
def create_product(manager_UUID: str, product_data: dict | ProductCreate, db: Session = Depends(sessions.get_db_PRODUCTS)):
    try:
        return CRUD.create_product(db=db, creator_UUID=manager_UUID, product_data=product_data)
    except:
        raise HTTPException(status_code=408, detail="manager.py -> Не удалось создать новый товар!")
    