##########################################################################################
#                               ОСНОВНОЙ СВЯЗУЮЩИЙ МОДУЛЬ                                #
##########################################################################################

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from requiests_module.users import users         # Модуль операций с Пользователями
from requiests_module.auth import auth         # Модуль операций с Аутентификацией
from requiests_module.messanger import messanger        # Модуль операций с Чатами и Сообщениями
from requiests_module.products import products           # Модуль операций с Товарами

from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    username: str

class UserDB(User):
    password: str


# Ресурсы которым разрешено получать доступ к данному приложению (Серверу) согласно политике CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Связывает все маршруты
app.include_router(users)
app.include_router(auth)
app.include_router(messanger)
app.include_router(products)


@app.get('/', tags=['Main'])
async def get_text():
    return 'main APP!'


@app.post('/', tags=['Main'], response_model=User)
async def post_req(data: UserDB):
    return data