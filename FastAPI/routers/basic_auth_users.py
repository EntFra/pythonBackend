from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/basicauth",
                   tags=["basicauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password": "123456"
    },
        "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "654321"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])  
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED , 
            detail="Credenciales de autentación inválidas",
            headers={"WWW-Authentica": "Bearer"})
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    users_db = users_db.get(form.username)
    if not users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="No existe el usuario")
    
    user = search_user(form.username)
    if not form.password == user.password: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST , detail="Contraseña incorrecta")
    
    return {"access_token": user.username , "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user