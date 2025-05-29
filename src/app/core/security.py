from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from src.app.core.config import settings  # asegúrate de tener una SECRET_KEY en .env


# 🔑 Contexto de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 Clave y configuración JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 día


# 🔐 Hash de la contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# 🔍 Verificar contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 🎟️ Crear token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 🔐 Verificar y decodificar token JWT
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
