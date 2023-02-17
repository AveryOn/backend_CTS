# ORM-МОДЕЛИ ДЛЯ БАЗЫ ДАННЫХ ТОВАРА (PRODUCTS)

# Импорт инструментов из sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
# Импорт ядра BaseProducts для создания таблиц БД PRODUCTS
from database_module.engine import BaseProducts


# ТАБЛИЦА ГРУППА ТОВАРА (напрмиер: группа "зима")
class ProductGroup(BaseProducts):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True, unique=True)      # первичный ключ
    name = Column(String, index = True, unique=True)         # Наименование ГРУППЫ товара
    image = Column(String)       # превью-картинка ГРУППЫ товара
    description = Column(String)        # описание ГРУППЫ товара

    products = relationship("Product", back_populates="group")     # двусторонняя связь с товарами этой ГРУППЫ товаром

    def __repr__(self):
        return f"""ProductGroup(
        id={self.id!r}, 
        name={self.name!r}, 
        image={self.image!r}, 
        description={self.description!r},
        )"""


# ТАБЛИЦА КАТЕГОРИИ ТОВАРА (напрмиер: категория "головные уборы")
class ProductCategory(BaseProducts):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, unique=True)      # первичный ключ
    name = Column(String, index = True, unique=True)         # Наименование КАТЕГОРИИ товара
    image = Column(String)       # превью-картинка КАТЕГОРИИ товара
    description = Column(String)        # описание КАТЕГОРИИ товара

    products = relationship("Product", back_populates="category")     # двусторонняя связь с товарами этой КАТЕГОРИИ товаров

    def __repr__(self):
        return f"""ProductCategory(
        id={self.id!r}, 
        name={self.name!r}, 
        image={self.image!r}, 
        description={self.description!r},
        )"""


# ТАБЛИЦА С ТОВАРОМ
class Product(BaseProducts):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)      # первичный ключ
    article = Column(Integer, unique=True, index=True)      #   артикул товара. Используется в базе данных как идентификатор
    name = Column(String)       # наименование
    price = Column(Integer)     # цена
    group_name = Column(String, ForeignKey("groups.name"))          # имя группы товра
    category_name = Column(String, ForeignKey("categories.name"))       # имя категории товара
    tags = Column(String)       # теги
    creation_time = Column(Integer)     # Время создания товара
    creation_manager_UUID = Column(String)      # Уникальный Идентификатор сотрудника, который создал данный товар
    edit_time = Column(Integer)         # Время изменения (редактирования) товара
    discount = Column(Integer)      # скидка в процентах
    specifications = Column(String)     # характеристики
    country_origin = Column(String)         # страна производитель
    description = Column(String)        # полное описание
    images = Column(String)     # ссылки на картинки в firebase(или сами картинки)
    promotion = Column(String, default=None)      # обьект описания акции если она есть
    sold = Column(Integer)      # кол-во проданного
    rating = Column(Integer)        # оценка товара
    remains = Column(Integer)       # остаток товара

    comments = relationship("Comment", back_populates="parent_product")     # массив с комменатриями для каждого товара
    group = relationship("ProductGroup", back_populates="products")         # группа товара которой принадлежит товар
    category = relationship("ProductCategory", back_populates="products")        # категория товара которой принадлежит товар

    def __repr__(self):
        return f"""Product(
        id={self.id!r}, 
        article={self.article!r}, 
        name={self.name!r}, 
        price={self.price!r},
        group={self.group!r},
        category={self.category!r},
        tags={self.tags!r},
        creation_time={self.creation_time!r},
        creation_manager_UUID={self.creation_manager_UUID!r},
        edit_time={self.edit_time!r},
        country_origin={self.country_origin!r},
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

    id = Column(Integer, primary_key=True, unique=True, index=True)      # первичный ключ
    owner_id = Column(Integer, unique=True, index=True)     # идентификатор пользователя-создателя комментария
    owner_name = Column(String)       # имя пользователя-создателя
    owner_lastname = Column(String)       # фамилия пользователя-создателя
    data_text = Column(String)      # текст комментария (его тело)
    images = Column(String, default="[]")       # картинки в комментарии
    rating = Column(Integer)        # оценка товару
    creation_time = Column(String)      # время создания комментария
    parent_product_article = Column(Integer, ForeignKey("products.article"))      # article товара к которому принадлежит этот комментарий

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
        creation_time={self.creation_time!r},
        parent_product_id={self.parent_product_article!r},
        )"""


