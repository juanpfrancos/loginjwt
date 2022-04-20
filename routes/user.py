from fastapi import Body, APIRouter, Response, status
from schemas.user import UserSchema, UserLoginSchema
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from typing import List
from config.db import conn
from models.user import usuarios
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()

user = APIRouter()

# route handlers

@user.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    new_user={"nombre": user.nombre, "email":user.email}
    new_user["password"] = user.password
    result = conn.execute(usuarios.insert().values(new_user))
    conn.execute(usuarios.select().where(usuarios.columns.id_usuario == result.lastrowid)).first()    
    return signJWT(user.email)


@user.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    exist_email = conn.execute(usuarios.select().where(usuarios.columns.email == user.email)).first()
    if exist_email != None:
        input_pass = user.password
        pass_db = exist_email[3]
        if input_pass == pass_db:
            print('Logueado')
            return signJWT(user.email)
        else:
            print('PassIncorrect')
            return Response(status_code=400)
    else:
        print('usuario inexistente')
        return {"error": "Wrong login details!"}