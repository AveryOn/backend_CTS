####################################################################################################
#                                      МОДЕЛИ PYDANTIC ТОВАРОВ                                     #
####################################################################################################

# Инструменты pydantic
from pydantic import BaseModel

# Модель нигде не используется играет роль фундамента для обьекта Product
# (Product - условный обьект который обозначает один элемент Базы Данных PRODUCTS в таблице Product)
class ProductBase(BaseModel):
    pass


# Модель используется при создании нового товара МЕНЕДЖЕРОМ или ВЛАДЕЛЬЦЕМ сервиса
# Данная модель является телом запроса с клиентом и регламентирует какие поля должны быть
class ProductCreate(ProductBase):
    article: int
    name: str
    price: int
    group: dict
    category: dict
    tags: list
    creation_time: int
    creation_manager_UUID: str
    discount: int | None = None
    specifications: dict
    description: str
    images: list
    promotion: dict | None = None
    remains: int
    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True

# Модель используется для возврата на клиент. 
# Регламентирует какие поля должны быть у товара, который приходит на клиент
class Product(ProductBase):
    id: int
    article: int
    name: str
    price: int
    group: dict
    category: dict
    tags: list
    creation_time: int
    creation_manager_UUID: str
    edit_time: int | None = None
    discount: int | None = None
    specifications: dict
    description: str
    images: list
    promotion: dict | None = None
    sold: int = 0
    rating: int = 0
    remains: int
    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True

