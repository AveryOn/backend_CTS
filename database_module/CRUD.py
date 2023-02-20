####################################################################################################
#         МОДУЛЬ ВЗАИМОДЕЙСТВИЯ С БД. ПОЛУЧЕНИЕ /ОБНОВЛЕНИЕ /УДАЛЕНИЕ /СОЗДАНИЕ ДАННЫХ В БД        #
####################################################################################################

# Инструментов с FastAPI
from fastapi import HTTPException 

# Импорт ast модуля для приведения массивов и словарей со строкового в нативный
import ast

# Импорт ORM-таблиц
from database_module.models_user import User, UserCart, ServicePerson, UserChat
from database_module.models_product import Product, Comment, ProductGroup, ProductCategory

# Импорт Модулей с Pydantic-моделями
from schemas_module import user, user_cart, user_chat, product, message, comment

# Импорт зависимостей для авторизации и регистрации
from requiests_module.actions import auth

# Импорт инструментов с sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound


# Ключ доступа для модераторов. Применяется для подтверждения действия в качестве дополнительной верификации
MODERATOR_KEY: str = '9dd4f7a7efd9facf9cfbd59b2411c661'
# Ключ доступа для Владельца. Применяется для подтверждения действия в качестве дополнительной верификации
OWNER_KEY: str = '9c15a74bc8c1d16287da281402a2159d9cc1f1f18d7e26ddaba0357757b24df9'

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


# ПОЛУЧЕНИЕ всех пользователей
def get_all_users(db: Session) -> list[user.User]:
    try:
        return db.scalars(select(User)).all()
    except:
        raise HTTPException(status_code=500, detail="Не удалось получить список пользователей из БАЗЫ ДАННЫХ")


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
def update_user_all(db: Session, new_data: user.UserChangeData, user_id: int) -> user.User:
    # Создается копия данных с изменениями. Она не включает в себя поля с неопределенными значениями
    new_data_copy = new_data.dict(exclude_none=True, exclude_unset=True)
    db.execute(update(User).where(User.id == user_id).values(
        **new_data_copy
    ))
    db.commit()
    return user


# ===============================>>> БЛОК ОПЕРАЦИЙ ГРУППЫ ТОВАРА <<<=============================================


# Полуение ГРУППЫ товара
def get_group_product(db: Session, group_name: str):
    try:
        return db.execute(select(ProductGroup).filter_by(name=group_name)).scalar_one()
    except:
        raise HTTPException(status_code=404, detail="Не удалось получить группу товара с сервера!")


# Полуение СПИСКА ГРУПП товара
def get_all_group_product(db: Session) -> list[product.ProductGroup]:
    try:
        return db.scalars(select(ProductGroup)).all()
    except:
        raise HTTPException(status_code=404, detail="Не удалось получить список групп товара")


# ===============================>>> БЛОК ОПЕРАЦИЙ КАТЕГОРИИ ТОВАРА <<<=============================================


# Полуение КАТЕГОРИИ товара
def get_catrgory_product(db: Session, category_name: str):
    try:
        category = db.execute(select(ProductCategory).filter_by(name=category_name)).scalar_one()
        return category
    except:
        raise HTTPException(status_code=404, detail="Не удалось получить категорию товара с сервера!")


# Полуение СПИСКА КАТЕГОРИЙ товара
def get_all_category_product(db: Session) -> list[product.ProductCategory]:
    try:
        return db.scalars(select(ProductCategory)).all()
    except:
        raise HTTPException(status_code=404, detail="Не удалось получить список категорий товара с сервера!")


# ===============================>>> БЛОК ОПЕРАЦИЙ ТОВАРА <<<=============================================


# СОЗДАНИЕ нового товара в БД PRODUCTS
def create_product(db: Session, creator_UUID: str, product_data: dict | product.ProductCreate):
    # Дополнительная верификация на ключ доступа сотрудника
    if product_data.get("MODERATOR_KEY") == MODERATOR_KEY or product_data.get("MODERATOR_KEY") == OWNER_KEY:
        try:
            # Дополнительная порверка на совподение имени группы для создаваемого товара. 
            # Если имя группы (group_name) в теле запроса (product_data) не соответствует существующей в БД группе товара 
            # То товар не создается
            category = get_catrgory_product(db=db, category_name=product_data.get("category_name"))
            group = get_group_product(db=db, group_name=product_data.get("group_name"))
            if group and category:
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
                        category_name = str(product_data.get("category_name")),
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
                raise HTTPException(status_code=500, detail="Вы пытаетесь создать товар указав имя Группы или Категории товара, которой не существует!")
        except:
            raise HTTPException(status_code=404, detail="Вы пытаетесь создать товар указав имя Группы или Категории товара, которой не существует!")
    else:
        raise HTTPException(status_code=401, detail="Ключ модератора неверный!")


# ПОЛУЧЕНИЕ СПИСКА товара с БД PRODUCTS
def get_products(db: Session) -> list[product.Product]:
    products = db.scalars(select(Product)).all()
    return products


# ПОЛУЧЕНИЕ одного товара с БД PRODUCTS (по артикулу)
def get_one_product(db: Session, article: int):
    product = db.execute(select(Product).filter_by(article=article)).scalar_one()
    return product


# ИЗМЕНЕНИЕ (редактирование) товара
def edit_product(db: Session, article: int, edit_data: product.ProductChange):
    edit_data_copy = edit_data.dict(exclude_none=True, exclude_unset=True, exclude={'MODERATOR_KEY'})
    if edit_data.MODERATOR_KEY == MODERATOR_KEY or edit_data.MODERATOR_KEY == OWNER_KEY:
        try:
            db.execute(update(Product).where(Product.article == article).values(
                **edit_data_copy
            ))
            db.commit()
            return {"response_status": "Successful!"}
        except:
            raise HTTPException(status_code=500, detail="Не удалось зафиксировать изменения товара в Базе Данных")
    else:
        raise HTTPException(status_code=401, detail="Ключ модератора неверный!")


# УДАЛЕНИЕ товара 
def delete_product(db: Session, article: int, moderator_key: str):
    if moderator_key == MODERATOR_KEY or moderator_key == OWNER_KEY:
        try:
            product = get_one_product(db=db, article=article)
            db.delete(product)
            db.commit()
            return {"response_status": "Successful!"}
        except:
            raise HTTPException(status_code=500, detail="Не удалось удалить товар из Базы Данных!")
    else:
        raise HTTPException(status_code=401, detail="Ключ модератора неверный!")



# =====================================>>> БЛОК ОПЕРАЦИЙ С КОММЕНТАРИЯМИ <<<=============================================

# Функция вычисляет средний рейтинг относительно отзывов
def computed_rating(comments: list) -> (float | int) :
    sum = 0
    count = 0
    for comment in comments:
        sum += comment.rating
        count += 1
    rating_product = sum / count
    return rating_product


# СОЗДАНИЕ комментария. На Момент создания нового отзыва о товаре пользователем в этой функции
# автоматически высчитывается средняя оценка товара относительно всех отзывов включая новый
def create_comment(db: Session, comment_data: comment.CommentCreate):
    try:
        comment = Comment(**comment_data.dict(exclude_none=True, exclude_unset=True))
        db.add(comment)
        db.commit()
        db.refresh(comment)
    except:
        raise HTTPException(status_code=500, detail="Не удалось отправить комментарий в Базу Данных")
    try:
        # Получаем товар с базы данных чтобы получить все комментарии с оценками и высчитать общую среднюю оценку товара
        product = get_one_product(db=db, article=comment.parent_product_article)
        rating_product = computed_rating(product.comments)
    except:
        raise HTTPException(status_code=500, detail="Произошла ошибка при вычислении рейтинга товара")
    try:
        # Обновление оценки товара относительно высчитанного среднего значения
        db.execute(update(Product).where(Product.article == comment_data.parent_product_article).values(
            rating = rating_product
        ))
        db.commit()
        return {"response_status": "Successful!"}
    except:
        raise HTTPException(status_code=500, detail="Не удалось обновить рейтинг товара в Базе Данных")


# ИЗМЕНЕНИЕ комментария
def edit_comment(db: Session, data_comment: comment.CommentChange, comment_id: int):
    edit_data_copy = data_comment.dict(exclude_none=True, exclude_unset=True)
    try:
        try:
            # Обновляем тело комментария в Базе Данных
            db.execute(update(Comment).where(Comment.id == comment_id).values(
                **edit_data_copy
            ))
            # Фиксация транзации
            db.commit()
        except:
            raise HTTPException(status_code=500, detail="Не удалось обновить тело комментария")
        try:
            # Получаем товар с базы данных чтобы получить все комментарии с оценками и высчитать общую среднюю оценку товара
            product = get_one_product(db=db, article=data_comment.parent_product_article)
            update_rating_product = computed_rating(product.comments)
            db.execute(update(Product).where(Product.article == data_comment.parent_product_article).values(
                rating = update_rating_product
            ))
            # Фиксация транзации
            db.commit()
            return {"response_status": "Successful!"}
        except:
            raise HTTPException(status_code=500, detail="Произошла ошибка при вычислении рейтинга товара")
    except:
        raise HTTPException(status_code=500, detail="Не удалось редактировать комментарий")


# ПОЛУЧЕНИЕ СПИСКА комментариев 
def get_all_comments(db: Session, article: int) -> list[comment.Comment]:
    product = db.execute(select(Product).filter_by(article=article)).scalar_one()
    return product.comments


# УДАЛЕНИЕ комментария. Удалять комментарии могут все роли (пользователи, модераторы и владелец сервиса)
def delete_comment(db: Session, comment_id: int, article: int):
    try:
        comment = db.get(Comment, comment_id)
        # Дополнительная проверка чтобы товар наверняка соответствовал удаляемому комментарию  
        if comment.parent_product.article == article:
            db.delete(comment)
            db.commit()
        else:
            raise HTTPException(status_code=500, detail=f"Ошибка сервера. Обнаружена рассинхронизация связи между товаром с артикулом: {article} и комментарием с id: {comment_id}")
        try:
            product = get_one_product(db=db, article=article)
            rating_product = computed_rating(product.comments)
            db.execute(update(Product).where(Product.article == article).values(
                rating = rating_product
            ))
            db.commit()
            db.refresh(product)
            return {"response_status": "Successful!"}
        except:
            raise HTTPException(status_code=500, detail="Произошла ошибка при вычислении рейтинга товара")
    except:
        raise HTTPException(status_code=500, detail="Не удалось удалить комментарий")


# ===============================>>> БЛОК ОПЕРАЦИЙ МЕССЕНДЖЕРА <<<=============================================


# СОЗДАНИЕ нового чата ПОЛЬЗОВАТЕЛЯ
def create_new_chat(db: Session, data_chat: user_chat.UserChatCreate):
    try:
        chats = db.scalars(select(UserChat)).all()
        return chats
        # user_chats: list[dict] = user.chats
        # new_chat = UserChat(**data_chat.dict())
        # db.add(new_chat)
        # db.commit()
        # db.refresh(new_chat)
        # return {"response_status": "Successful!"}
    except:
        raise HTTPException(status_code=500, detail="Не удалось создать новый чат")


# ПОЛУЧЕНИЕ всех чатов ПОЛЬЗОВАТЕЛЯ
def get_all_chats_user(db: Session, user_id: int) -> list:
    # сначала получаем текущего пользователя
    user: User = db.execute(select(User).filter_by(id=user_id)).scalar_one()
    return user.chats

# ПОЛУЧЕНИЕ всех чатов СОТРУДНИКА
def get_all_chats_manager(db: Session, manager_UUID: str):
    # сначала получаем текущего сотрудника
    service_person: ServicePerson = db.execute(select(ServicePerson).filter_by(UUID=manager_UUID)).scalar_one()
    return service_person.chats



# ===============================>>> БЛОК ОПЕРАЦИЙ СОТРУДНИКОВ (МЕНЕДЖЕРОВ/МОДЕРАТОРОВ) <<<=============================================



# Создание новой ГРУППЫ товара
def create_group_product(db: Session, data_group: product.ProductGroupCreate):
    try:
        if(data_group.MODEATOR_KEY == MODERATOR_KEY or data_group.MODEATOR_KEY == OWNER_KEY):
            new_group = ProductGroup(name = data_group.name, description=data_group.description, image=data_group.image)
            db.add(new_group)
            db.commit()
            db.refresh(new_group)
            return new_group
        else:
            raise HTTPException(status_code=401, detail="Ключ модератора неверный!")
    except:
        raise HTTPException(status_code=400, detail="Не удалось создать группу товара!")


# Создание новой КАТЕГОРИИ товара
def create_category_product(db: Session, data_category: product.ProductCategoryCreate):
    try:
        if(data_category.MODEATOR_KEY == MODERATOR_KEY or data_category.MODEATOR_KEY == OWNER_KEY):
            new_category = ProductCategory(name = data_category.name, description=data_category.description, image=data_category.image)
            db.add(new_category)
            db.commit()
            db.refresh(new_category)
            return new_category
        else:
            raise HTTPException(status_code=401, detail="Ключ модератора неверный!")
    except:
        raise HTTPException(status_code=400, detail="Не удалось создать категорию товара!")


# Получение данных СОТРУДНИКА по username
def get_service_person(db: Session, username: str):
    # Получение пользователя по username
    try:
        return db.execute(select(ServicePerson).filter_by(username = username)).scalar_one()
    except NoResultFound:
        # Поднимает исключение если СОТРУДНИК с таким username не найден
        raise HTTPException(status_code=404, detail=f"Пользователь с логином '{username}' не найден!")
 

# ПОЛУЧЕНИЕ всех СОТРУДНИКОВ с бд
def get_all_service_person(db: Session):
    try:
        return db.scalars(select(ServicePerson)).all()
    except:
        raise HTTPException(status_code=500, detail="Не удалось получить список сотрудников сервиса!")


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