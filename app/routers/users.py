from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate, UserResponse, UserUpdate , PostResponse

from app import crud
from app.security import require_admin
from app.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)




@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)



@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return crud.get_all_users(db)

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = crud.get_user(db, user_id)

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, user_id, user)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = crud.delete_user(db, user_id)

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "Deleted Successfully"
    }



@router.get("/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Session = Depends(get_db)):

    user = crud.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return crud.get_posts_by_user(db, user_id)