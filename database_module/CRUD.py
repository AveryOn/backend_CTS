####################################################################################################
#         МОДУЛЬ ВЗАИМОДЕЙСТВИЯ С БД. ПОЛУЧЕНИЕ /ОБНОВЛЕНИЕ /УДАЛЕНИЕ /СОЗДАНИЕ ДАННЫХ В БД        #
####################################################################################################

# Импорт ORM-таблиц
from models_user import User, UserCart, UserChat, Message
from models_product import Product, Comment

# Импорт Pydantic-моделей
from schemas_module import user, user_cart, user_chat, product, message, comment

# Импорт тулов с sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select, update


#===========>>>   ВЗАИМОДЕЙСТВИЕ С БАЗОЙ ДАННЫХ  -  USERS.db   <<<==================

# Создание пользователя и корзины товаров

def create_user(db: Session, user: user.UserCreate):
    pass


