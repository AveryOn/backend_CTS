####################################################################################################
#         МОДУЛЬ ВЗАИМОДЕЙСТВИЯ С БД. ПОЛУЧЕНИЕ /ОБНОВЛЕНИЕ /УДАЛЕНИЕ /СОЗДАНИЕ ДАННЫХ В БД        #
####################################################################################################

# Инструментов с FastAPI
from fastapi import HTTPException 

# Импорт ORM-таблиц
from database_module.models_user import User, UserCart, ServicePerson
from database_module.models_product import Product, Comment
from database_module.models_messanger import UserChat, Message

# Импорт Модулей с Pydantic-моделями
from schemas_module import user, user_cart, user_chat, product, message, comment

# Импорт зависимостей для авторизации и регистрации
from requiests_module.actions import auth

# Импорт инструментов с sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select, update


#===========>>>   ВЗАИМОДЕЙСТВИЕ С БАЗОЙ ДАННЫХ  -  USERS.db   <<<==================

# Создание пользователя и корзины товаров
def create_user(db: Session, user: user.UserCreate):
    hashed_password = auth.hash_password(user.password)
    new_user = User(email = user.email, username = user.username, hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    new_cart = UserCart(owner_id = new_user.id, data = '[]')
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_user


# Создание нового сотрудника рабочего персонала
def create_service_person(db: Session, service_person: user.ServicePersonCreate) -> user.ServicePerson:
    hashed_password = auth.hash_password(service_person.password)
    new_service_person = ServicePerson(
        UUID = service_person.UUID,
        role = service_person.role,
        email = service_person.email, 
        name = service_person.name,
        lastname = service_person.lastname,
        username = service_person.username, 
        hashed_password = hashed_password,
        # allows = service_person.allows,
        sex = service_person.sex
    )
    db.add(new_service_person)
    db.commit()
    db.refresh(new_service_person)
    return new_service_person