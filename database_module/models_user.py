# ORM-МОДЕЛИ ДЛЯ БАЗЫ ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ (USERS)

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from engine import BaseUsers

# ТАБЛИЦА С ПОЛЬЗОВАТЕЛЯМИ
class User(BaseUsers):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    lastname = Column(String)
    image = Column(String)
    sex = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # двусторонняя связь с таблицей КОРЗИНЫ данного пользователя
    cart = relationship("UserCart", back_populates="owner")
    # двусторонняя связь с таблицей ЧАТОВ данного пользователя
    chats = relationship("UserChat", back_populates="owner")

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
    owner_id = Column(Integer, ForeignKey("users.id"))
    data = Column(String)
    # двусторонняя связь этой корзины с конкретным пользователем (ее владельцем)
    owner = relationship("User", back_populates="cart")

    # служебный метод для отладки
    def __repr__(self):
        return f"""UserCart( id={self.id!r}, owner_id={self.owner_id!r}, data={self.data!r} )"""


# ТАБЛИЦА ЧАТОВ ПОЛЬЗОВАТЕЛЕЙ
class UserChat(BaseUsers):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id_1 = Column(Integer, ForeignKey('users.id'))
    user_id_2 = Column(Integer, ForeignKey('users.id'))
    creation_time = Column(String)

    # двусторонняя связь данного чата с конкретным пользователем 
    owner = relationship("User", back_populates="chats")
    # массив всех сообщений данного чата
    messages = relationship("Message", back_populates="parent_chat")

    # служебный метод для отладки
    def __repr__(self):
        return f"""UserChat( 
            id={self.id!r}, 
            user_id_1={self.user_id_1!r}, 
            user_id_2={self.user_id_2!r}, 
            creation_time={self.creation_time!r},
        )"""


# ТАБЛИЦА С СООБЩЕНИЯМИ
class Message(BaseUsers):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id_from = Column(Integer, ForeignKey("users.id"))
    user_id_to = Column(Integer, ForeignKey("users.id"))
    creation_time = Column(String)
    data = Column(String)
    parent_chat_id = Column(Integer, ForeignKey("chats.id"))

    # двусторонняя связь данного сообщения с чатом-родителем, которому оно принадлежит 
    parent_chat = relationship("UserChat", back_populates="messages")

    # служебный метод для отладки
    def __repr__(self):
        return f"""Message( 
            id={self.id!r}, 
            user_id_from={self.user_id_from!r}, 
            user_id_to={self.user_id_to!r}, 
            creation_time={self.creation_time!r},
            data={self.data!r},
            parent_chat_id={self.parent_chat_id!r},
        )"""