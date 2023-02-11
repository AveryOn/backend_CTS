# Здесь распологаются движкки баз данных
# Всего две Базы Данных, Одна для товаров другая для Пользователей и чатов


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

####################################################################################################
#                                   Движок для USERS БД                                            #
####################################################################################################

engine_users = create_engine(
    'sqlite+pysqlite:///DB/USERS.db',
    echo=True,
    future=True,
    connect_args={"check_same_thread": False}
)

session_users = sessionmaker(autoflush=False, autocommit=False, bind=engine_users)
BaseUsers = declarative_base()


####################################################################################################
#                                   Движок для PRODUCTS БД                                         #
####################################################################################################

engine_products = create_engine(
    'sqlite+pysqlite:///DB/PRODUCTS.db',
    echo=True,
    future=True,
    connect_args={"check_same_thread": False}
)

session_products = sessionmaker(autoflush=False, autocommit=False, bind=engine_users)
BaseProducts = declarative_base()