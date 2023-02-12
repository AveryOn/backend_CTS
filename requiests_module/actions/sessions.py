####################################################################################################
#                             МОДУЛЬ ДЛЯ ЗАПУСКА СЕССИЙ БД                            #
####################################################################################################

# Импорт сессий всех ДБ
from database_module.engine import session_messanger, session_products, session_users


# Создание сессии для подключение к БД USERS.db
def get_db_USERS():
    db = session_users()
    try:
        yield db
    finally:
        db.close()


# Создание сессии для подключение к БД PRODUCTS.db
def get_db_PRODUCTS():
    db = session_products()
    try:
        yield db
    finally:
        db.close()


# Создание сессии для подключение к БД MESSANGER.db
def get_db_MESSANGER():
    db = session_messanger()
    try:
        yield db
    finally:
        db.close()