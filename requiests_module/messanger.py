##########################################################################################
#                      МАРШРУТ ДЛЯ ОПЕРАЦИЙ С ЧАТАМИ, СООБЩЕНИЯМИ                        #
##########################################################################################

# Инструменты FastAPI
from fastapi import APIRouter, Depends

# Импорт pydantic-моделей
from schemas_module.message import MessageCreate, Message

# Импорт CRUD функций
from database_module import CRUD

# Импорт инструментов 
from sqlalchemy.orm import Session

# Импорт Модуля Actions
from requiests_module.actions import sessions


# Создание экземпляра маршрута, все пути которые относятся к этому маршруту 
# будут начинаться с /messanger
messanger = APIRouter(
    prefix='/messanger',
    tags=["messanger"],
)


@messanger.post('/send-message/')
def send_message(data_message: MessageCreate, db: Session = Depends(sessions.get_db_USERS)):
    return CRUD.create_new_message(db=db, data_message=data_message)


@messanger.get('/{chat_id}/get-chat-messages/', response_model=list[Message])
def get_chat_messages(chat_id: int, db: Session = Depends(sessions.get_db_USERS)) -> list[Message]:
    return CRUD.get_chat_messages(db=db, chat_id=chat_id)




