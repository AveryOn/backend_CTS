##########################################################################################
#                               ОСНОВНОЙ СВЯЗУЮЩИЙ МОДУЛЬ                                #
##########################################################################################

from fastapi import FastAPI
from users import users         # Модуль операций с Пользователями
from auth import auth         # Модуль операций с Аутентификацией
from messanger import messanger        # Модуль операций с Чатами и Сообщениями
from products import products           # Модуль операций с Товарами

app = FastAPI()
# Связывает все маршруты
app.include_router(users)
app.include_router(auth)
app.include_router(messanger)
app.include_router(products)


@app.get('/', tags=['Main'])
async def get_text():
    return 'hello text!'

@app.post('/', tags=['Main'])
async def post_req(data: str):
    return data