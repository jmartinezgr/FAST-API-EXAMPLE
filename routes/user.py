from fastapi import APIRouter


user = APIRouter()

@user.get("/")
def hello_world():
    return {"message": "Hello World"}