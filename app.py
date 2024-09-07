from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="FastAPI CRUD",
    openapi_tags=[{
        "name": "User",
        "description": "Endpoints related to users"
    }]
)

app.include_router(user, prefix="/user")    