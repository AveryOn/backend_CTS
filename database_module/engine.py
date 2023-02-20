# Здесь распологаются движкки баз данных
# Всего 3 Базы Данных, которые лежат  ./database_module/DB/ 
# 1) для товаров, 
# 2) для Пользователей и их Корзин с товарами
# 3) для Чатов и сообщений

# Импорт инструментов sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

####################################################################################################
#                                   ДВИЖОК ДЛЯ USERS БД                                            #
####################################################################################################


engine_users = create_engine(
    'sqlite+pysqlite:///database_module/DB/USERS.db',
    echo=True,
    future=True,
    connect_args={"check_same_thread": False}
)

# Для запуска сесии с БД USERS 
session_users = sessionmaker(autoflush=False, autocommit=False, bind=engine_users)
# Для декларативного сопоставления ORM-таблиц с Python. В модуле models_user таблицы строятся на основе этой переменной
BaseUsers = declarative_base()


####################################################################################################
#                                   ДВИЖОК ДЛЯ PRODUCTS БД                                         #
####################################################################################################


engine_products = create_engine(
    'sqlite+pysqlite:///database_module/DB/PRODUCTS.db',
    echo=True,
    future=True,
    connect_args={"check_same_thread": False}
)

# Для запуска сесии с БД PRODUCTS 
session_products = sessionmaker(autoflush=False, autocommit=False, bind=engine_products)
# Для декларативного сопоставления ORM-таблиц с Python. В модуле models_product таблицы строятся на основе этой переменной
BaseProducts = declarative_base()


# ####                                                      !!! НЕ ИСПОЛЬЗУЕТСЯ !!!
####################################################################################################
#                                   ДВИЖОК ДЛЯ MESSANGER БД                                        #
####################################################################################################

# engine_messanger = create_engine(
#     'sqlite+pysqlite:///database_module/DB/MESSANGER.db',
#     echo=True,
#     future=True,
#     connect_args={"check_same_thread": False}
# )

# # Для запуска сесии с БД MESSANGER 
# session_messanger = sessionmaker(autoflush=False, autocommit=False, bind=engine_messanger)
# # Для декларативного сопоставления ORM-таблиц с Python. В модуле models_messanger таблицы строятся на основе этой переменной
# BaseMessanger = declarative_base()