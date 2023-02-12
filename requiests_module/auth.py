##########################################################################################
#                          МАРШРУТ ДЛЯ ОПЕРАЦИЙ С АУТЕНТИФИКАЦИЕЙ                        #
##########################################################################################

from fastapi import APIRouter, Depends
from schemas_module.user import UserCreate, User
from database_module import CRUD
from requiests_module.actions import sessions
from sqlalchemy.orm import Session

auth = APIRouter(
    tags=["auth"],
)


# Создание нового пользователя
@auth.post('/registration/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(sessions.get_db_USERS)):
    return CRUD.create_user(db=db, user=user)


@auth.get('/auth/')
def get_user():
    return {'auth': 'hello! text!'}