####################################################################################################
#                                 МОДЕЛИ PYDANTIC ДЛЯ ПОЛЬЗОВАТЕЛЯ                                 #
####################################################################################################

# Инструменты pydantic
from pydantic import BaseModel

# Модель нигде не используется играет роль фундамента для обьекта user
# (user - условный обьект который обозначает один элемент Базы Данных USERS в таблице User)
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
    role: str = 'user'
    name: str | None=None
    lastname: str | None=None
    image: str | None=None
    sex: str | None=None
    is_active: bool | None=None
    chats_id: int | None=None

    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True


####################################################################################################
#                             МОДЕЛИ PYDANTIC ДЛЯ СЛУЖЕБНОГО ПЕРСОНАЛА                             #
####################################################################################################


# Модель нигде не используется играет роль фундамента для обьекта ServicePerson 
# (ServicePerson - условный обьект который обозначает один элемент Базы Данных USERS в таблице ServicePerson)
class ServicePersonBase(BaseModel):
    pass


# Модель для создания нового сотрудника. Создать аккаунт сотрудника может только владелец
class ServicePersonCreate(ServicePersonBase):
    UUID: str
    email: str
    name: str
    lastname: str
    username: str
    password: str
    # allows: dict
    SECRET_KEY: str
    sex: str


# Модель для чтения пользователя из БД / Возврата на клиент
class ServicePerson(ServicePersonBase):
    id: int
    username: str
    email: str
    role: str
    allows: dict
    name: str
    lastname: str
    image: str | None=None
    sex: str
    is_active: bool = False
    chats_id: int | None=None

    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True