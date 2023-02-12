####################################################################################################
#         МОДУЛЬ ВЗАИМОДЕЙСТВИЯ С БД. ПОЛУЧЕНИЕ /ОБНОВЛЕНИЕ /УДАЛЕНИЕ /СОЗДАНИЕ ДАННЫХ В БД        #
####################################################################################################

# Импорт ORM-таблиц
from models_user import User, UserCart, UserChat, Message
from models_product import Product, Comment

# Импорт Pydantic-моделей
from schemas_module import user, user_cart, user_chat, product, message, comment

# Импорт зависимостей для авторизации и регистрации
from requiests_module.actions import auth

# Импорт тулов с sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select, update


#===========>>>   ВЗАИМОДЕЙСТВИЕ С БАЗОЙ ДАННЫХ  -  USERS.db   <<<==================

# Создание пользователя и корзины товаров

def create_user(db: Session, user: user.UserCreate) -> user.User:
    hashed_password = auth.hash_password(user.password)
    user_db = User(email = user.email, username = user.username, hashed_password = hashed_password)

