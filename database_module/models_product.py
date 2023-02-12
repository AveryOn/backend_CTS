# ORM-МОДЕЛИ ДЛЯ БАЗЫ ДАННЫХ ТОВАРА (PRODUCTS)

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from engine import BaseProducts


# ТАБЛИЦА С ТОВАРОМ
class Product(BaseProducts):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)      # первичный ключ
    article = Column(Integer, unique=True, index=True)      #
    name = Column(String)       # наименование
    price = Column(Integer)     # цена
    group = Column(String)      # группа товара
    category = Column(String)       # категория товара
    tags = Column(String)       # теги
    discount = Column(Integer)      # скидка в процентах
    specifications = Column(String)     # характеристики
    description = Column(String)        # полное описание
    images = Column(String)     # ссылки на картинки в firebase(или сами картинки)
    promotion = Column(String, default=None)      # обьект описания акции если она есть
    sold = Column(Integer)      # кол-во проданного
    rating = Column(Integer)        # оценка товара
    remains = Column(Integer)       # остаток товара

    comments = relationship("Comment", back_populates="parent_product")     # массив с комменатриями для каждого товара

    def __repr__(self):
        return f"""Product(
        id={self.id!r}, 
        article={self.article!r}, 
        name={self.name!r}, 
        price={self.price!r},
        group={self.group!r},
        category={self.category!r},
        tags={self.tags!r},
        discount={self.discount!r},
        specifications={self.specifications!r},
        description={self.description!r},
        images={self.images!r},
        promotion={self.promotion!r},
        sold={self.sold!r},
        rating={self.rating!r},
        remains={self.remains!r},
        )"""


# ТАБЛИЦА С КОММЕНТАРИЯМИ ДЛЯ КАЖДОГО ТОВАРА
class Comment(BaseProducts):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)      # первичный ключ
    owner_id = Column(Integer, unique=True, index=True)     # идентификатор пользователя-создателя комментария
    owner_name = Column(String)       # имя пользователя-создателя
    owner_lastname = Column(String)       # фамилия пользователя-создателя
    data_text = Column(String)      # текст комментария (его тело)
    images = Column(String, default=None)       # картинки в комментарии
    rating = Column(Integer)        # оценка товара
    parent_product_id = Column(Integer, ForeignKey("products.id"))      # идентификатор товара к которому принадлежит этот комментарий

    parent_product = relationship("Product", back_populates="comments")     # двусторонняя связь с родительским товаром

    def __repr__(self):
        return f"""Comment(
        id={self.id!r}, 
        owner_id={self.owner_id!r}, 
        owner_name={self.owner_name!r}, 
        owner_lastname={self.owner_lastname!r},
        data_text={self.data_text!r},
        images={self.images!r},
        rating={self.rating!r},
        parent_product_id={self.parent_product_id!r},
        )"""