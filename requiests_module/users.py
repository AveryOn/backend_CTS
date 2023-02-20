##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ С ПОЛЬЗОВАТЕЛЯМИ                         #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Инструменты pydantic
from pydantic import BaseModel

# Импорт Моделей Pydantic
from schemas_module.user import UserCreate, User, UserChangeData, UserChangePassword, ProductCart
from schemas_module.comment import CommentCreate, CommentChange
from schemas_module.user_chat import UserChatCreate, UserChat

# Импорт инструментов 
from sqlalchemy.orm import Session

# Импорт модуля взаимодействия с базами данных
from database_module import CRUD

# Импорт Модуля Actions
from requiests_module.actions import sessions
from requiests_module.actions.auth import get_current_user

# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /users
user = APIRouter(
    prefix='/user',
    tags=["user"],
)

# ===============================>>> ОПЕРАЦИИ С КОРЗИНОЙ <<<============================================= 


# Получение данных о коризне ПОЛЬЗОВАТЕЛЯ
@user.get('/{user_id}/cart/')
def get_cart_user(user_id: int, db: Session = Depends(sessions.get_db_USERS)):
    try:
        return CRUD.get_user_cart(db=db, user_id=user_id)
    except:
        raise HTTPException(status_code=400, detail="Не удалось получить доступ к корзине пользователя") 


# Добавление товара в корзину ПОЛЬЗОВАТЕЛЯ
@user.patch('/add-product/{login}/')
def add_cart_products(login: str, product: dict | ProductCart,  db: Session = Depends(sessions.get_db_USERS)) -> dict:
    try:
        append_product = CRUD.add_cart_product(db=db, login=login, product=product)
        return  append_product
    except:
        raise HTTPException(status_code=401, detail="Не удалось добавить товар в корзину!")

class UpdateCart(BaseModel):
    update_cart: list

# Удаление товаров с корзины. update_cart - массив корзины уже не включаюший удаляемые товары.
# Удаление товара с массива должно происходить на клиенте после чего этот массив отправляется на Бэкенд 
@user.put('/remove_cart/{user_id}/')
def remove_cart_product(user_id: int, update_cart: list | UpdateCart,  db: Session = Depends(sessions.get_db_USERS)) -> dict:
    # приведение входных данных cart_list в массив
    cart_list = list(update_cart.update_cart)
    return CRUD.remove_cart_product(db=db, user_id=user_id, update_cart=cart_list)


# ===============================>>> ОПЕРАЦИИ С ПОЛЬЗОВАТЕЛЕМ <<<=============================================


# Создание нового ПОЛЬЗОВАТЕЛЯ
@user.post('/registration/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(sessions.get_db_USERS)):
    try:
        return CRUD.create_user(db=db, user=user)
    except:
        raise HTTPException(status_code=401, detail="Не удалось зарегистрировать нового пользователя!")


# ПОЛУЧЕНИЕ всех пользователей
@user.get('/get-all-users/', response_model=list[User])
def get_all_users(db: Session = Depends(sessions.get_db_USERS)):
    return CRUD.get_all_users(db=db)


# Получение данных зарегестрированного ПОЛЬЗОВАТЕЛЯ. 
# С клиента приходит заголовок вида:  'Authorization': 'Bearer ' + access_token
@user.get('/me/', response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user


# Обновление НЕСКОЛЬКИХ данных ПОЛЬЗОВАТЕЛЯ
@user.put('/user-update/{user_id}/', response_model=User)
def update_user(user_id: int, new_data: UserChangeData, db: Session = Depends(sessions.get_db_USERS)) -> User:
    try:
        return CRUD.update_user_all(db=db, new_data=new_data, user_id=user_id)
    except:
        raise HTTPException(status_code=401, detail=f"Не удалось обновить данные пользоваетеля {user.username}!")   


# Обновление пароля ПОЛЬЗОВАТЕЛЯ
@user.patch('/user-update-password/{user_id}/')
def update_user_password(user_id: int, new_data: UserChangePassword, db: Session = Depends(sessions.get_db_USERS)) -> dict:
    try:
        return CRUD.update_user_password(db=db, new_data=new_data, user_id=user_id)
    except:
        raise HTTPException(status_code=401, detail="Не удалось обновить пароль!")


# Удаление ПОЛЬЗОВАТЕЛЯ
@user.delete('/user-delete/{user_id}')
def delete_user(user_id: int, db: Session = Depends(sessions.get_db_USERS)) -> dict:
    try:
        CRUD.delete_user(db=db, user_id=user_id)
        return {"response_status": 'Successful!'}
    except:
        raise HTTPException(status_code=400, detail="Не удалось удалить пользователя из базы")


# ===============================>>> ОПЕРАЦИИ С КОММЕНТАРИЯМИ <<<=============================================


# СОЗДАНИЕ комментария. Идентификатор передается в теле запроса
@user.post('/create-comment/')
def create_comment(comment_data: CommentCreate, db: Session = Depends(sessions.get_db_PRODUCTS)):
    return CRUD.create_comment(db=db, comment_data=comment_data)


# ИЗМЕНЕНИЕ (редактирование) комментария
@user.put('/edit-comment/{comment_id}/')
def edit_comment(comment_id: int, data_comment: CommentChange, db: Session = Depends(sessions.get_db_PRODUCTS)):
    return CRUD.edit_comment(db=db, data_comment=data_comment, comment_id=comment_id)


# ===============================>>> ОПЕРАЦИИ С МЕССЕНДЖЕРОМ <<<=============================================

# СОЗДАНИЕ нового чата
@user.post('/create-new-chat/')
def create_new_chat(data_chat: UserChatCreate, db: Session = Depends(sessions.get_db_USERS)):
    return CRUD.create_new_chat(db=db, data_chat=data_chat)


# ПОЛУЧЕНИЕ всех чатов пользователя
@user.get('/{user_id}/get-all-chats/')
def get_all_chats_user(user_id: int, db: Session = Depends(sessions.get_db_USERS)) -> list:
    return CRUD.get_all_chats_user(db=db, user_id=user_id)





