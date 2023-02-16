####################################################################################################
#         МОДУЛЬ ВЗАИМОДЕЙСТВИЯ С БД. ПОЛУЧЕНИЕ /ОБНОВЛЕНИЕ /УДАЛЕНИЕ /СОЗДАНИЕ ДАННЫХ В БД        #
####################################################################################################

# Инструментов с FastAPI
from fastapi import HTTPException 

# Импорт ast модуля для приведения массивов и словарей со строкового в нативный
import ast

# Импорт ORM-таблиц
from database_module.models_user import User, UserCart, ServicePerson
from database_module.models_product import Product, Comment, ProductGroup
from database_module.models_messanger import UserChat, Message

# Импорт Модулей с Pydantic-моделями
from schemas_module import user, user_cart, user_chat, product, message, comment

# Импорт зависимостей для авторизации и регистрации
from requiests_module.actions import auth

# Импорт инструментов с sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound


#===========>>>   ВЗАИМОДЕЙСТВИЕ С БАЗОЙ ДАННЫХ  -  USERS.db   <<<==================


# ===============================>>> БЛОК ОПЕРАЦИЙ С КОРЗИНОЙ <<<=============================================

# Получение корзины текущего ПОЛЬЗОВАТЕЛЯ 
def get_user_cart(db: Session, user_id: int) -> user.UserCart:
    try:
        user = db.get(User, user_id)
        cart_data: dict = user.cart[0]
        return cart_data
    except:
        raise HTTPException(status_code=400, detail="Не удалось получить доступ к корзине пользователя")        


# Добавление товара в корзину авторизованного ПОЛЬЗОВАТЕЛЯ
def add_cart_product(db: Session, login: str, product: dict) -> dict:
    # Получение по username
    try:
        user = db.execute(select(User).filter_by(username = login)).scalar_one()
        # Переводим тип данных корзины с str -> в list
        cart = ast.literal_eval(user.cart[0].data)
        # Проверка не допускает повторения товара в корзине
        if not product in cart:
            cart.append(product)
            user.cart[0].data = str(cart)
            db.commit()
            return product
        else:
            return {"message": "Товар не добавлен. Такой товар уже имеется"}
    except NoResultFound:
        # Получение по email
        try:
            user = db.execute(select(User).filter_by(email = login)).scalar_one()
            # Переводим тип данных корзины с str -> в list
            cart: list = ast.literal_eval(user.cart[0].data)
            # Проверка не допускает повторения товара в корзине
            if not product in cart:
                cart.append(product)
                user.cart[0].data = str(cart)
                db.commit()
                return product
            else:
                return {"message": "Товар не добавлен. Такой товар уже имеется"}
        except NoResultFound:
            # Поднимает исключение если пользователь с таким логином не найден
            raise HTTPException(status_code=404, detail=f"Пользователь с логином '{login}' не найден!")       


# Удаление товаров с корзины
def remove_cart_product(db: Session, user_id: int, update_cart: list) -> dict:
    user = db.get(User, user_id)
    if(not str(user.cart[0].data) == str(update_cart)):
        user.cart[0].data = str(update_cart)
        db.commit()
        db.refresh(user)
        return {"status_response": "Successful!"}
    else:
        return {"status_response": "Не удалось удалить товар с корзины!"}


# ===============================>>> БЛОК ОПЕРАЦИЙ ПОЛЬЗОВАТЕЛЕЙ <<<=============================================


# Создание пользователя и корзины товаров
def create_user(db: Session, user: user.UserCreate):
    hashed_password = auth.hash_password(user.password)
    new_user = User(email = user.email, username = user.username, hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    new_cart = UserCart(owner_id = new_user.id, data = '[]')
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_user


# Удаление ПОЛЬЗОВАТЕЛЯ с базы данных USERS
def delete_user(db: Session, user_id: int) -> None:
    try:
        user = db.get(User, user_id)
        db.delete(user)
        db.commit()
    except:
        raise HTTPException(status_code=400, detail=f"Не удалось выполнить DELETE-запрос, пользователь {user.username} не удален")        


# Получение данных ПОЛЬЗОВАТЕЛЯ по логину
def get_user(db: Session, login: str) -> User:
    # Получение пользователя по логину. Логином может быть как email, так и username, поэтому первый блок try->except
    # нужен для поиска пользователя по username, а второй вложенный блок try->except для получения по email

    # Получение по username
    try:
        return db.execute(select(User).filter_by(username = login)).scalar_one()
    except NoResultFound:
        # Получение по email
        try:
            return db.execute(select(User).filter_by(email = login)).scalar_one()
        except NoResultFound:
            # Поднимает исключение если пользователь с таким логином не найден
            raise HTTPException(status_code=404, detail=f"Пользователь с логином '{login}' не найден!")


# Получение данных ПОЛЬЗОВАТЕЛЯ по идентификатору (первичноу ключу БД)
def get_user_by_id(db: Session, id: int) -> user.User:
    try:
        return db.get(User, id)
    except:
        raise HTTPException(status_code=404, detail="Невозможно получить пользователя по ID")


# Обновление пароля ПОЛЬЗОВАТЕЛЯ
def update_user_password(db: Session, new_data: user.UserChangePassword, user_id: int) -> dict:
    # Обновление password, если пришло в запросе new_data
    try:
        if not new_data.password is None:
            user = db.get(User, user_id)
            if(not auth.verify_password(new_data.password, user.hashed_password)):
                hashed_password = auth.hash_password(new_data.password)
                user.hashed_password = hashed_password
                db.execute(update(User).where(User.id == user_id).values(
                    hashed_password = hashed_password
                ))
                db.commit()
                return {"response_status": "Пароль успешно обновлен!"}
            else:
                return {"response_status": "Не удалось обновить пароль! Этот пароль уже установлен!"}
    except:
        return {"response_status": "Не удалось обновить пароль!"}


# Обновление нескольких НЕОБЯЗАТЕЛЬНЫХ данных ПОЛЬЗОВАТЕЛЯ (Если пользователь обновляет не один атриубут например username, а несколько)
def update_user_all(db: Session, new_data: user.UserChangeData, user: user.User) -> user.User:
    # Обновление username, если пришло в запросе new_data
    if not new_data.username is None:
        user.username = new_data.username

    # Обновление email, если пришло в запросе new_data
    if not new_data.email is None:
        user.email = new_data.email
    
    # Обновление name, если пришло в запросе new_data
    if not new_data.name is None:
        user.name = new_data.name
    
    # Обновление lastname, если пришло в запросе new_data
    if not new_data.lastname is None:
        user.lastname = new_data.lastname
    
    # Обновление image, если пришло в запросе new_data
    if not new_data.image is None:
        user.image = new_data.image
    
    # Обновление sex, если пришло в запросе new_data
    if not new_data.sex is None:
        user.sex = new_data.sex
    
    db.execute(update(User).where(User.id == user.id).values(
        username=user.username,
        email = user.email,
        name = user.name,
        lastname = user.lastname,
        image = user.image,
        sex = user.sex,
    ))
    db.commit()
    return user


# ===============================>>> БЛОК ОПЕРАЦИЙ ГРУППЫ ТОВАРА <<<=============================================


# Полуение группы товара
def get_group_product(db: Session, group_name: str):
    try:
        group = db.execute(select(ProductGroup).filter_by(name=group_name)).scalar_one()
        return group
    except:
        raise HTTPException(status_code=500, detail="Не удалось получить группу товара с сервера!")


# ===============================>>> БЛОК ОПЕРАЦИЙ ТОВАРА <<<=============================================


# СОЗДАНИЕ нового товара
def create_product(db: Session, creator_UUID: str, product_data: dict | product.ProductCreate) -> product.Product:
    try:
        # Дополнительная порверка на совподение имени группы для создаваемого товара. 
        # Если имя группы (group_name) в теле запроса (product_data) не соответствует существующей в БД группе товара 
        # То товар не создается
        group = get_group_product(db=db, group_name=product_data.get("group_name"))
        if group:
            # Дополнительная проверка типов для некоторых полей. 
            # Если поле в значении None то переводить в строку его не нужно, а если обьект или массив то нужно
            promotion = None
            if not product_data.get("promotion") is None:
                promotion = str(product_data.get("promotion"))
            else:
                promotion = None
            try:
                product = Product(
                    article = product_data.get("article"),
                    name = product_data.get("name"),
                    price = product_data.get("price"),
                    group_name = str(product_data.get("group_name")),
                    category = str(product_data.get("category")),
                    tags = str(product_data.get("tags")),
                    creation_time = product_data.get("creation_time"),
                    creation_manager_UUID = creator_UUID,
                    discount = product_data.get("discount"),
                    specifications = str(product_data.get("specifications")),
                    country_origin = product_data.get("country_origin"),
                    description = product_data.get("description"),
                    images = str(product_data.get("images")),
                    promotion = promotion,
                    remains = product_data.get("remains"),
                )
                db.add(product)
                db.commit()
                db.refresh(product)
                return product
            except:
                raise HTTPException(status_code=500, detail="Не удалось создать новый товар")
        else:
            raise HTTPException(status_code=500, detail="Вы пытаетесь создать товар указав имя Группы товара, которая не существует!")
    except:
        raise HTTPException(status_code=500, detail="Не удалось создать новый товар. Что-то пошло не так")


# ПОЛУЧЕНИЕ товара с БД PRODUCTS
def get_products(db: Session) -> list[product.Product]:
    products = db.scalars(select(Product)).all()
    return products



# ===============================>>> БЛОК ОПЕРАЦИЙ СОТРУДНИКОВ (МЕНЕДЖЕРОВ/МОДЕРАТОРОВ) <<<=============================================

# Ключ доступа для модераторов. Применяется для подтверждения действия в качестве дополнительной верификации
MODERATOR_KEY = '9dd4f7a7efd9facf9cfbd59b2411c661'


# Создание новой группы товара
def create_group_products(db: Session, data_group: product.ProductGroupCreate):
    try:
        if(data_group.MODEATOR_KEY == MODERATOR_KEY):
            new_group = ProductGroup(name = data_group.name, description=data_group.description, image=data_group.image)
            db.add(new_group)
            db.commit()
            db.refresh(new_group)
            return new_group
        else:
            raise HTTPException(status_code=401, detail="Ключ модератора неверный!")
    except:
        raise HTTPException(status_code=400, detail="Не удалось создать группу товара!")


# Получение данных СОТРУДНИКА по username
def get_service_person(db: Session, username: str) -> user.ServicePerson:
    # Получение пользователя по username
    try:
        return db.execute(select(ServicePerson).filter_by(username = username)).scalar_one()
    except NoResultFound:
        # Поднимает исключение если СОТРУДНИК с таким username не найден
        raise HTTPException(status_code=404, detail=f"Пользователь с логином '{username}' не найден!")
 


# ===============================>>> БЛОК ОПЕРАЦИЙ ВЛАДЕЛЬЦА <<<=============================================


# Создание нового сотрудника рабочего персонала
def create_service_person(db: Session, service_person: user.ServicePersonCreate) -> user.ServicePerson:
    hashed_password = auth.hash_password(service_person.password)
    new_service_person = ServicePerson(
        UUID = service_person.UUID,
        role = service_person.role,
        email = service_person.email, 
        name = service_person.name,
        lastname = service_person.lastname,
        username = service_person.username, 
        hashed_password = hashed_password,
        # allows = service_person.allows,
        sex = service_person.sex
    )
    db.add(new_service_person)
    db.commit()
    db.refresh(new_service_person)
    return new_service_person