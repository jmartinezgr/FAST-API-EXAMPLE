from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet

# Clave para encriptar contraseñas
key = Fernet.generate_key()
f = Fernet(key)

# Instancia de APIRouter
user = APIRouter()

@user.get("/",response_model=list[User])
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
        
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)

@user.get("/{id}", response_model=User)
def get_user(id: int):
    result = conn.execute(users.select().where(users.c.id == id)).first()
    
    if result:
        user = {
            "id": result[0],
            "name": result[1],
            "email": result[2],
            "password": result[3]
        }
        return JSONResponse(content=user, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "User not found"})

@user.post("/", response_model=User)
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
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=user_dict)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "User not found"})
    
@user.put("/{id}", response_model=User)
def update_user(id: int, user: User):
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": f.encrypt(user.password.encode("utf-8"))
    }
    
    result = conn.execute(users.update().values(new_user).where(users.c.id == id))
    conn.commit()
    
    if result.rowcount:
        user_updated = conn.execute(users.select().where(users.c.id == id)).first()
        
        user_dict = {
            "id": user_updated[0],
            "name": user_updated[1],
            "email": user_updated[2],
            "password": user_updated[3]
        }
        
        return JSONResponse(content=user_dict, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "User not found"})    
    
@user.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str):
    result = conn.execute(users.delete().where(users.c.id == id))
    conn.commit()
    
    if result.rowcount:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,  content={"error": "User not found"})