##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ ВЛАДЕЛЬЦА СЕРВИСА                        #
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

owner = APIRouter(
    prefix='/owner',
    tags=["owner"],
)

SECRET_KEY = '$2b$12$KPH.9tF5ycOszX5TI7CzkuausE30Os2M4NQ3lOcYGAnKXDDUef9LS'

# Для создания владельца
# SECRET_KEY: 'ce2b1cab3a9a1cc34ea66b50e2a766c68f054d81920807da4615c7bd665094e8'
# password: '$2b$12$6Oafob5Y4Pe1ZYqF.FIN8eI3u5KzOzMGKNpVcm.yhAzPw787lumXO'
# UUID: '53f48706-4fed-4251-b3ec-2d89bc386eab'


# При создании нового сотрудника (например Модератора), Владелец вводит его данные, и указывает ключ который доступен только ему
# Этот ключ служит для дополнительной безопасности, и авторизации владельца. Также он предостерегает сервис от возможного
# взлома клиента и изменения важных учетных данных

# Создание нового сотрудника
@owner.post('/create-new-person/', response_model=ServicePerson)
def create_service_person(service_person: ServicePersonCreate, db: Session = Depends(sessions.get_db_USERS)):
    if (auth.verify_password(input_password = service_person.SECRET_KEY, hashed_password = SECRET_KEY)):
        new_person = CRUD.create_service_person(db=db, service_person=service_person)
        return new_person
    else:
        raise HTTPException(status_code=408, detail='Ключ Владельца не верный!')    
