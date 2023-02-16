##########################################################################################
#                               ОСНОВНОЙ СВЯЗУЮЩИЙ МОДУЛЬ                                #
##########################################################################################

# Инструменты FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импорт отдельных маршрутов с операциями для путей
from requiests_module.owner import owner         # Модуль операций Владельца
from requiests_module.manager import manager         # Модуль операций Модератора
from requiests_module.users import user         # Модуль операций с Пользователями
from requiests_module.auth import auth         # Модуль операций с Аутентификацией
from requiests_module.messanger import messanger        # Модуль операций с Чатами и Сообщениями
from requiests_module.products import products           # Модуль операций с Товарами


app = FastAPI()

# Связывает все маршруты в один роутер
app.include_router(user)
app.include_router(auth)
app.include_router(messanger)
app.include_router(products)
app.include_router(owner)
app.include_router(manager)


# Ресурсы которым разрешено получать доступ к данному приложению (Серверу) согласно политике CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080", 
        "http://localhost:8081",
        "http://192.168.1.148:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get('/', tags=['Main'])
async def get_text():
    return 'main APP!'


