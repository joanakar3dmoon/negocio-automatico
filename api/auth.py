from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from .models import Role, User

SECRET = "superclave-cambia-en-produccion"
ALGO = "HS256"
TOKEN_MINUTES = 60 * 24

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

USERS_DB = {
    "admin@r3dm.com": User(email="admin@r3dm.com", password=pwd.hash("admin123"), role=Role.ADMIN),
    "cliente@r3dm.com": User(email="cliente@r3dm.com", password=pwd.hash("cliente123"), role=Role.CLIENTE),
}


def autenticar(email: str, password: str):
    user = USERS_DB.get(email)
    if user is None or not pwd.verify(password, user.password):
        return None
    return user


def crear_token(user: User):
    expires = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES)
    return jwt.encode({"email": user.email, "role": user.role.value, "exp": expires}, SECRET, algorithm=ALGO)


def usuario_actual(token: str = Depends(oauth2)):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        email = data.get("email")
        if not email or email not in USERS_DB:
            raise credentials_error
        return USERS_DB[email]
    except (JWTError, KeyError):
        raise credentials_error


def requiere_admin(user: User = Depends(usuario_actual)):
    if user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Solo admin")
    return user
