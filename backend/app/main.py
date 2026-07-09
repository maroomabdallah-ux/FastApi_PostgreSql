from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base
from app.database import engine
from app.routers import users
from app.routers import posts
from app.routers import auth
from app.routers import products
from app.routers import user_products


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI CRUD"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(user_products.router)


@app.get("/")
def home():
    return {
        "message": "FastAPI PostgreSQL"
    }