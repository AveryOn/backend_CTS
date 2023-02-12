####################################################################################################
#                               МОДУЛЬ ЗАВИСИМОСТЕЙ ДЛЯ АВТОРИЗАЦИИ                                #
####################################################################################################

# Импорт Вспомогательных тулов с fastapi
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Импорт библиотек для валидации паролей и токенов
from jose import jwt, JWTError
from passlib.context import CryptContext

# Импорт даты для работы с токенами
from datetime import datetime, timedelta




passlib = CryptContext(schemes=["bcrypt"], deprecated="auto")
