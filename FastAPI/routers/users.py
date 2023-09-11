from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

#Inicia el server: python -m uvicorn users:app --reload

#Entidad: User
class User(BaseModel):
    id:int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1,name="Ivan", surname="Prieto", url="google.es", age=30),
         User(id=2,name="Moure", surname="Dev", url="mouredev.com", age=30)]

@router.get("/usersjson")
async def usersjson():
    return [{"name":"Ivan", "surname":"Prieto", "url":"google.es","age":30},
            {"name":"Moure", "surname":"Dev", "url":"mouredev.com", "age":30}]

@router.get("/users")
async def users():
    return users_list

@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

@router.get("/userquery/")
async def user(id: int):
    return search_user(id)

@router.post("/user/", status_code=201)
async def user(user: User):
    if type(search_user(user.id))==User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")

    else:   
        users_list.append(user)
        return user

@router.put("/user/")
async def user(user: User):
    for saved_user in users_list:
        if saved_user.id == user.id:
          return {"user modified"} 

@router.delete("/user/{id}")
async def user(id:int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
         del users_list[index]


def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"Usuario no encontrado"}
    

