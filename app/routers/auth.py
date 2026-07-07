from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserLogin
from app import crud
from app.security import create_access_token
from app.security import get_current_user
from app.models import User
from app.schemas import UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = crud.authenticate_user(
        db,
        user.email,
        user.password
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "user_id": db_user.id,
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user