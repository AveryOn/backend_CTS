####################################################################################################
#         МОДУЛЬ ВЗАИМОДЕЙСТВИЯ С БД. ПОЛУЧЕНИЕ /ОБНОВЛЕНИЕ /УДАЛЕНИЕ /СОЗДАНИЕ ДАННЫХ В БД        #
####################################################################################################

# Импорт ORM-таблиц
from models_user import User, UserCart, UserChat, Message
from models_product import Product, Comment

# Импорт Pydantic-моделей


# Импорт тулов с sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select, update