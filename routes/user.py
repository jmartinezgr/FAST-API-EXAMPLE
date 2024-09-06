from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet

# Clave para encriptar contraseñas
key = Fernet.generate_key()
f = Fernet(key)

# Instancia de APIRouter
user = APIRouter()

@user.get("/")
def get_users():
    result = conn.execute(users.select()).fetchall()
    
    data = [
        {
            "id": item[0],
            "name": item[1],
            "email": item[2],
            "password": item[3]
        }
        
        for item in result
    ]
    
    return {"data": data}

@user.post("/")
def create_user(user: User):
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": f.encrypt(user.password.encode("utf-8"))
    }
    
    # Insertar nuevo usuario
    result = conn.execute(users.insert().values(new_user))
    conn.commit()
    
    # Seleccionar el nuevo usuario creado
    user_created = conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
    
    # Convertir el resultado en un diccionario
    if user_created:
        user_dict = {
            "id": user_created[0],
            "name": user_created[1],
            "email": user_created[2],
            "password": user_created[3]
        }
        return user_dict
    else:
        return {"error": "User not found"}