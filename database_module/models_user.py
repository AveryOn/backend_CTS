# ORM-МОДЕЛИ ДЛЯ БАЗЫ ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ (USERS)

# Импорт инструментов из sqlalchemy
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
# Импорт ядра BaseUsers для создания таблиц БД USERS
from database_module.engine import BaseUsers

# ТАБЛИЦА С ПОЛЬЗОВАТЕЛЯМИ
class User(BaseUsers):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)      # первичный ключ (идентификатор)  (АВТОМАТИЧЕСКИЙ)
    username = Column(String, unique=True, index=True)      # Никнэйм пользователя  (!! ОБЯЗАТЕЛЬНЫЙ !!)
    email = Column(String, unique=True, index=True)     # Эл. почта  (!! ОБЯЗАТЕЛЬНЫЙ !!)
    name = Column(String)       #  Имя пользоваателя  (НЕОБЯЗАТЕЛЬНЫЙ)
    lastname = Column(String)       # Фамилия пользователя  (НЕОБЯЗАТЕЛЬНЫЙ)
    image = Column(String)      # Аватарка аккаунта пользователя  (НЕОБЯЗАТЕЛЬНЫЙ)
    sex = Column(String)        # Пол пользователя  (НЕОБЯЗАТЕЛЬНЫЙ)
    hashed_password = Column(String)        # Хеш пароля  (!! ОБЯЗАТЕЛЬНЫЙ !!)
    chats_id = Column(String)       # Массив с id чатов которые есть у данного пользователя  (НЕОБЯЗАТЕЛЬНЫЙ)
    is_active = Column(Boolean, default=True)       # Флаг - активен ли пользователь (эксперементальный атрибут)  (НЕОБЯЗАТЕЛЬНЫЙ)
    # двусторонняя связь с таблицей КОРЗИНЫ данного пользователя
    cart = relationship("UserCart", back_populates="cart")      # Массив корзины с товаром

    # служебный метод для отладки
    def __repr__(self):
        return f"""User(
            id={self.id!r},
            username={self.username!r},
            email={self.email!r},
            name={self.name!r},
            lastname={self.lastname!r},
            image={self.image!r},
            sex={self.sex!r},
            hashed_password={self.hashed_password!r},
            is_active={self.is_active!r},
        )"""


# ТАБЛИЦА С КОРЗИНАМИ ПОЛЬЗОВАТЕЛЕЙ
class UserCart(BaseUsers):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))      # Идентификатор пользователя которому принадлежит данная корзина
    data = Column(String)       # Массив с товарами
    # двусторонняя связь этой корзины с конкретным пользователем (ее владельцем)
    cart = relationship("User", back_populates="cart")

    # служебный метод для отладки
    def __repr__(self):
        return f"""UserCart( id={self.id!r}, owner_id={self.owner_id!r}, data={self.data!r} )"""



# from engine import engine_users, BaseUsers

# from models_user import User, UserChat, UserCart, Message

# BaseUsers.metadata.create_all(engine_users) 

#  tomas = User(email="tomas@example.com", username='tomas123', hashed_password='aidjfoa83q')

#  alex = User(email='alex@example.com', username='alex142', hashed_password='aionf91-093')

#  from sqlalchemy.orm import Session

#  session = Session(autoflush=False, autocommit=False, bind=engine_users)


# message2 = Message(user_id_from=3, user_id_to=2, creation_time='25.05.2023 12:35', data= "{text: 'Oh yeah, Hello!', images: None}", parent_chat_id=1)
