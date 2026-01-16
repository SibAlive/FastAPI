import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt # шифрование/декодирование
from passlib.context import CryptContext # безопасное хэширование паролей
from passlib.hash import bcrypt
from dotenv import load_dotenv


# Загружаем переменные из .env в os.environ
load_dotenv()

users_db = {"admin": {
                "username": "admin",
                "hashed_password": bcrypt.hash("qwerty") # Хэш пароля "qwerty"
}}

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


# Сравнивает обычный пароль с его хэшем
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Возвращает пользователя из БД
def get_user(username):
    if username in users_db:
        return users_db[username]
    return None


# Аутентифицирует пользователя и возвращает его объект при успехе
def authenticate_user(username, password):
    user = get_user(username)
    if not user or not verify_password(password, user.get("hashed_password")):
        return False
    return user


#  Создает JWT-токен и шифрует данные
def create_access_token(data, expires_delta):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



# Защита endpoints
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    print("Получен токен:", credentials.credentials)  # ← Для отладки
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user =  get_user(username)
    if user is None:
        raise credentials_exception
    return user