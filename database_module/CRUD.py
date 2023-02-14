####################################################################################################
#         МОДУЛЬ ВЗАИМОДЕЙСТВИЯ С БД. ПОЛУЧЕНИЕ /ОБНОВЛЕНИЕ /УДАЛЕНИЕ /СОЗДАНИЕ ДАННЫХ В БД        #
####################################################################################################

# Импорт ORM-таблиц
from database_module.models_user import User, UserCart
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
    user_db = User(email = user.email, username = user.username, hashed_password = hashed_password)
    db.add(user_db)
    print(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db