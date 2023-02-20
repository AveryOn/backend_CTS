####################################################################################################
#                                      МОДЕЛИ PYDANTIC СООБЩЕНИЙ                                   #
####################################################################################################


# Инструменты pydantic
from pydantic import BaseModel

# Модель нигде не используется играет роль фундамента для обьекта Message
# (Message - условный обьект который обозначает один элемент Базы Данных USERS в таблице Message)
class MessageBase(BaseModel):
    pass


# Модель для создания нового сообщения
class MessageCreate(MessageBase):
    user_id_from: int
    user_id_to: int
    creation_time: str
    data: str      # Пример data: '{"text": 'текст сообщения', "images": 'массив с картинками'}'
    parent_chat_id: int


# Модель для возврата созданного сообщения на клиент
class Message(MessageBase):
    id: int
    user_id_from: int
    user_id_to: int
    creation_time: str
    data: str      # Пример data:  {"text": 'текст сообщения', "images": 'массив с картинками'} 
    parent_chat_id: int
    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True





