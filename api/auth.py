from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from .models import User, Role
import os

SECRET = os.getenv("JWT_SECRET", "superclave")
ALGO = "HS256"

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

USERS_DB = {
    "admin@r3dm.com": User(email="admin@r3dm.com", password=pwd.hash("admin123"), role=Role.ADMIN),
    "cliente@r3dm.com": User(email="cliente@r3dm.com", password=pwd.hash("cliente123"), role=Role.CLIENTE),
}

def autenticar(email: str, password: str):
    if email not in USERS_DB:
        return None
    user = USERS_DB[email]
    if not pwd.verify(password, user.password):
        return None
    return user

def crear_token(user: User):
    return jwt.encode({"email": user.email, "role": user.role}, SECRET, algorithm=ALGO)

def usuario_actual(token: str = Depends(oauth2)):
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        email = data["email"]
        return USERS_DB[email]
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

def requiere_admin(user: User = Depends(usuario_actual)):
    if user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Solo admin")
    return user