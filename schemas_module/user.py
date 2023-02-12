####################################################################################################
#                                 МОДЕЛЬ PYDANTIC ДЛЯ ПОЛЬЗОВАТЕЛЯ                                 #
####################################################################################################

from pydantic import BaseModel

# Модель нигде не используется играет роль фундамента для обьекта user
class UserBase(BaseModel):
    pass


# Модель для создания нового пользователя
class UserCreate(UserBase):
    email: str
    username: str
    password: str


# Модель для чтения пользователя из БД / Возврата на клиент
class User(UserBase):
    id: int
    username: str
    email: str
    name: str | None=None
    lastname: str | None=None
    image: str | None=None
    sex: str | None=None
    is_active: bool | None=None

    class Config:
        orm_mode = True
        