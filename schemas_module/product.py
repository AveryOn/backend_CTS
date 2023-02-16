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
# !!! Обрати внимение, что поля category и group - являются строками. Но это так потому что 
# когда создается новый товар то в его теле передается не обькт catrgory и group а их название
# для проверки на то существует ли такая группа или категория в базе данных. Если нет то на клиент возвращается 404
class ProductCreate(ProductBase):
    article: int
    name: str
    price: int
    group_name: str
    category: str
    tags: list
    creation_time: int
    creation_manager_UUID: str
    discount: int | None = None
    specifications: dict
    country_origin: str
    description: str
    images: list
    promotion: dict | None = None
    remains: int
    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True

# Модель используется для возврата на клиент. 
# Регламентирует какие поля должны быть у товара, который приходит на клиент
# Поля 
#   promotion и specifications
# являются словарями но в строковом формате. Клиент уже парсит их в нужный тип данных
# Поля  tags, images  списки но возвращаются на клиент как строки
class Product(ProductBase):
    id: int
    article: int
    name: str
    price: int
    group_name: str
    category: str
    tags: str
    creation_time: int
    creation_manager_UUID: str
    edit_time: int | None = None
    discount: int | None = None
    specifications: str
    country_origin: str
    description: str
    images: str
    promotion: str | None = None
    sold: int | None = None
    rating: int | None = None
    remains: int
    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True


# Модель нигде не используется играет роль фундамента для обьекта ProductGroup
# (ProductGroup - условный обьект который обозначает один элемент Базы Данных PRODUCTS в таблице ProductGroup)
class ProductGroupBase(BaseModel):
    pass


# Модель для создания группы товара. Группа товара обьединяет все товары конкретной тематики например зимняя группа товаров
# или электротовары.
# MODEATOR_KEY - служит для дополнительной верификации
class ProductGroupCreate(ProductGroupBase):
    name: str
    description: str | None = None
    image: str
    MODEATOR_KEY: str


# Модель используется для возврата группы товара на клиент
class ProductGroup(ProductGroupBase):
    id: int
    name: str
    description: str | None = None
    image: str


