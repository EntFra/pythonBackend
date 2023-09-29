from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "hisdgfibsjkdgbsdgjklsd"

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username:str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str

users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "$2a$12$6utcXl7LUiRl7C1bm0JOD.BvhHRV0TiayOm0d4JhxIhONoGxqrLz."

    },
        "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "$2a$12$LbzlAShtN9OXclbQhF2TCOT1MySsZsQ7aepo.USyz6WGpnFQSSfJa"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])  

    
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED , 
            detail="Credenciales de autentación inválidas",
            headers={"WWW-Authentica": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    
    except JWTError:
        raise exception

    return search_user(username)

    
async def current_user(user: User = Depends(auth_user)):

    return user    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    users_db = users_db.get(form.username)
    if not users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="No existe el usuario")
    
    user = search_user(form.username)  
    if crypt.verify(form.password, user.password): 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST , detail="Contraseña incorrecta")

    access_token = {"sub":user.username,
                   "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM) , "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

