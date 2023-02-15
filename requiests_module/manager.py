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
from schemas_module.user import ServicePerson, ServicePersonCreate

# Импорт Модуля Actions
from requiests_module.actions import sessions, auth


# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /manager
manager = APIRouter(
    prefix='/manager',
    tags=["manager"],
)

# Получение данных зарегестрированного пользователя. 
# С клиента приходит заголовок вида:  'Authorization': 'Bearer ' + access_token
@manager.get('/me/', response_model=ServicePerson)
def get_user(user: ServicePerson = Depends(auth.get_current_service_person)):
    return user