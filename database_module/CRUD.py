####################################################################################################
#         МОДУЛЬ ВЗАИМОДЕЙСТВИЯ С БД. ПОЛУЧЕНИЕ /ОБНОВЛЕНИЕ /УДАЛЕНИЕ /СОЗДАНИЕ ДАННЫХ В БД        #
####################################################################################################

# Инструментов с FastAPI
from fastapi import HTTPException 

# Импорт ORM-таблиц
from database_module.models_user import User, UserCart, ServicePerson
from database_module.models_product import Product, Comment
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


# Получение корзины текущего ПОЛЬЗОВАТЕЛЯ 
def get_user_cart(db: Session, user_id: int) -> user.UserCart:
    try:
        user = db.get(User, user_id)
        cart_data: dict = user.cart[0]
        return cart_data
    except:
        raise HTTPException(status_code=400, detail="Не удалось получить доступ к корзине пользователя")        


# Обновление пароля ПОЛЬЗОВАТЕЛЯ
def update_user_password(db: Session, new_data: user.UserChangePassword, user_id: int) -> None:
    # Обновление password, если пришло в запросе new_data
    if not new_data.password is None:
        user = db.get(User, user_id)
        hashed_password = auth.hash_password(new_data.password)
        user.hashed_password = hashed_password
        db.execute(update(User).where(User.id == user_id).values(
            hashed_password = hashed_password
        ))
        db.commit()

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


# Получение данных СОТРУДНИКА по логину
def get_service_person(db: Session, username: str) -> user.ServicePerson:
    # Получение пользователя по username
    try:
        return db.execute(select(ServicePerson).filter_by(username = username)).scalar_one()
    except NoResultFound:
        # Поднимает исключение если СОТРУДНИК с таким username не найден
        raise HTTPException(status_code=404, detail=f"Пользователь с логином '{username}' не найден!")

# Обновление данных пользователя
def user_update():
    pass

#===========>>>  БЛОК ОПЕРАЦИЙ ВЛАДЕЛЬЦА  <<<==================


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