# backend_CTS (В разработке)
backend for an online store - Current Target Sale

### Архитектура Бэкенда

https://github.com/AveryOn/backend_CTS  -  github.com

Backend:

    requests_module     # Основной модуль для работы с фронтендом
        ---- __init__.py
        ---- auth.py               # Авторизация, регистрация и пр.
        ---- chat.py               # Чат, мессенджер
        ---- products.py           # Обработка товаров, добавление, удаление и пр.
        ---- users.py              # Обработка пользователей

    models_module:      # Модуль с моделями pydantic
        ---- __init__.py
        ---- users__class.py       # Обьекты характерные для пользователей (всё что к ним относится)
        ---- massage__class.py     # Обьекты относящиеся к чатам/мессенджерам
        ---- products__class.py    # Обьекты для работы с товарами
        ---- auth__class.py        # Обьекты для работы с Авторизацией

    database_module:    # Модуль СУБД
        ---- __init__.py    
        ---- engine_users__orm.py   # движок БД для users
        ---- models__orm.py         # ORM-модели БД (ТАБЛИЦЫ БД)
        ---- crud__orm.py           # Функции создания, получения, обновления и удаления данных в БД

