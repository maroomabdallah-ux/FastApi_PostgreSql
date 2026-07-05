from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI CRUD"
)

app.include_router(users.router)


@app.get("/")
def home():

    return {
        "message": "FastAPI PostgreSQL"
    }