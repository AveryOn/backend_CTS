####################################################################################################
#                             МОДЕЛЬ PYDANTIC ДЛЯ КОРЗИНЫ ПОЛЬЗОВАТЕЛЯ                             #
####################################################################################################

# Инструменты pydantic
from pydantic import BaseModel

# Модель нигде не используется играет роль фундамента для обьекта user_cart
class UserCartBase(BaseModel):
    pass


# Модель для создания КОРЗИНЫ пользователя
class UserCartCreate(UserCartBase):
    data: list[dict] = []


# Модель для чтения КОРЗИНЫ конкретного пользователя из БД / Возврата на клиент
class UserCart(UserCartBase):
    id: int
    owner_id: int
    data: list[dict] = []

    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode=True
