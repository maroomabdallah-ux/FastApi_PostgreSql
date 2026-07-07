from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PostCreate, PostResponse
from app import crud
from app.security import get_current_user
from app.models import User


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post)


@router.get("/", response_model=list[PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(current_user.id)
    print(current_user.email)
    print(current_user.role)

    return crud.get_all_posts(db)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):

    post = crud.get_post(db, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):

    post = crud.delete_post(db, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return {
        "message": "Post deleted successfully"
    }