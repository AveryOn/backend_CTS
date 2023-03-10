####################################################################################################
#                                 МОДЕЛИ PYDANTIC ДЛЯ ПОЛЬЗОВАТЕЛЯ                                 #
####################################################################################################

# Инструменты pydantic
from pydantic import BaseModel

# Модель нигде не используется играет роль фундамента для обьекта user
# (user - условный обьект который обозначает один элемент Базы Данных USERS в таблице User)
class UserBase(BaseModel):
    pass


# Модель для получения входа в свою учетную запись (личный кабинет) для всех Пользователей
class UserLogin(UserBase):
    username: str
    password: str

    class Config:
        orm_mode = True

# Модель для создания нового пользователя
class UserCreate(UserBase):
    email: str
    username: str
    password: str
    creation_time: str


# Модель для аннотации аргументов которые приходят с клиента (Для ОБНОВЛЕНИЯ данных ПОЛЬЗОВАТЕЛЯ)
# Все поля включенные в эту модель могут быть ИЗМЕНЕНЫ для конкретного пользователя в базе данных
class UserChangeData(UserBase):
    username: str | None=None
    email: str | None=None
    name: str | None=None
    lastname: str | None=None
    image: str | None=None
    sex: str | None=None
    edit_time: str

    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True

# Модель для аннотации аргументов которые приходят с клиента (Для УДАЛЕНИЯ данных ПОЛЬЗОВАТЕЛЯ)
# Все поля включенные в эту модель могут быть УДАЛЕНЫ для конкретного пользователя в базе данных
class UserDeleteData(UserBase):
    name: str | None=None
    lastname: str | None=None
    image: str | None=None
    sex: str | None=None
    edit_time: str


class UserChangePassword(UserBase):
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
    creation_time: str
    edit_time: str | None=None
    is_active: bool | None=None

    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True


# Модель нигде не используется играет роль фундамента для обьекта user_cart
# (user_cart - условный обьект который обозначает один элемент Базы Данных USERS в таблице UserCart)
class UserCartBase(BaseModel):
    pass

# Модель КОРЗИНЫ для возврата на клиент
class UserCart(UserCartBase):
    id: int
    owner_id: int
    data: list[dict]

    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True

# Модель используется для записи товара в корзину ПОЛЬЗОВАТЕЛЯ.
# На клиенте и в общей базе товаров модель имеет больше атрибутов. id и article -> нужны для идентификации товара
class ProductCart(BaseModel):
    id: int
    article: int
    name: str
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


class ServicePersonLogin(ServicePersonBase):
    UUID: str
    KEY_ACCESS: str
    username: str
    password: str

# Модель для создания нового сотрудника. Создать аккаунт сотрудника может только владелец
class ServicePersonCreate(ServicePersonBase):
    UUID: str
    role: str
    email: str
    name: str
    lastname: str
    username: str
    password: str
    allows: str
    OWNER_KEY: str
    sex: str
    creation_time: str


# Модель для чтения сотрудника из БД / Возврата на клиент
class ServicePerson(ServicePersonBase):
    id: int
    UUID: str
    username: str
    email: str
    role: str
    allows: str | None=None
    action_history: str | None=None
    name: str
    lastname: str
    image: str | None=None
    sex: str
    creation_time: str
    edit_time: str | None=None
    is_active: bool = False

    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True