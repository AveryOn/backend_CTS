####################################################################################################
#                                   МОДЕЛИ PYDANTIC ДЛЯ МЕССЕНДЖЕРА                                #
####################################################################################################


# Инструменты pydantic
from pydantic import BaseModel


# Модель нигде не используется играет роль фундамента для обьекта UserChat
# (UserChat - условный обьект который обозначает один элемент Базы Данных USERS в таблице UserChat)
class UserChatBase(BaseModel):
    pass


# Модель используется для создания нового чата
class UserChatCreate(UserChatBase):
    user_id: int
    service_person_id: int
    creation_time: str
    class Config:
        orm_mode = True


class UserChat(UserChatBase):
    id: int
    user_id: int
    service_person_id: int
    creation_time: str
    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True

