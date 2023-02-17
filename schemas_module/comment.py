####################################################################################################
#                                 МОДЕЛИ PYDANTIC ДЛЯ КОММЕНТАРИЕВ                                 #
####################################################################################################

# Иснтрументы pydantic
from pydantic import BaseModel



# Модель нигде не используется играет роль фундамента для обьекта comment
# (comment - условный обьект который обозначает один элемент Базы Данных PRODUCTS в таблице Comment)
class CommentBase(BaseModel):
    pass


# Модель регламентирует какие поля необходимы для создания комментария
# Данная модель приходит с клиента в виде тела запроса
class CommentCreate(CommentBase):
    owner_id: int
    owner_name: str
    owner_lastname: str
    data_text: str | None=None
    images: str | None=None
    creation_time: str
    rating: int
    parent_product_article: int


# Данная модель используется как тело запроса для изменения/редактирования существующего комментария на клиенте
class CommentChange(CommentBase):
    # поля которые допустимо менять для комментария
    data_text: str | None=None
    images: str | None=None
    rating: int | None=None
    # данный атрибут не служит для изменения. Он отправляется на сервер для дополнительной проверки
    parent_product_article: int


# Модель для возврата комментария на клиент с базы данных
class Comment(CommentBase):
    id: int
    owner_id: int
    owner_name: str
    owner_lastname: str
    data_text: str | None=None
    images: str | None=None
    rating: int
    creation_time: str
    parent_product_article: int
    # orm_mode для корректного взаимодействия с БД
    class Config:
        orm_mode = True





