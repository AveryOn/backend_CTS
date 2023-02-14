# ORM-МОДЕЛИ ДЛЯ БАЗЫ ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ (MESSANGER)

# Импорт инструментов из sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
# Импорт ядра BaseMessanger для создания таблиц БД MESSANGER
from database_module.engine import BaseMessanger


# ТАБЛИЦА ЧАТОВ ПОЛЬЗОВАТЕЛЕЙ
class UserChat(BaseMessanger):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id_1 = Column(Integer)     # Идентификатор первого пользователя начавшего чат
    user_id_2 = Column(Integer)     # Идентификатор второго пользователя
    creation_time = Column(String)      # Время создания данного чата

    # массив всех сообщений данного чата
    messages = relationship("Message", back_populates="parent_chat")        # Массив сообщений данного чата

    # служебный метод для отладки
    def __repr__(self):
        return f"""UserChat( 
            id={self.id!r}, 
            user_id_1={self.user_id_1!r}, 
            user_id_2={self.user_id_2!r}, 
            creation_time={self.creation_time!r},
        )"""


# ТАБЛИЦА С СООБЩЕНИЯМИ
class Message(BaseMessanger):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id_from = Column(Integer)      # Идентификатор пользователя-ОТПРАВИТЕЛЯ данного сообщения
    user_id_to = Column(Integer)        # Идентификатор пользователя-ПОЛУЧАТЕЛЯ данного сообщения
    creation_time = Column(String)      # Время создания данного сообщения
    data = Column(String, default='{text: None, images: None}')       # Тело сообщения (Обьект в котором содержатся поля text и images)
    parent_chat_id = Column(Integer, ForeignKey("chats.id"))        # Идентификатор родительского чата которому принадлежит данное сообщение

    # двусторонняя связь данного сообщения с чатом-родителем, которому оно принадлежит 
    parent_chat = relationship("UserChat", back_populates="messages")       # Обьект родительского чата

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
