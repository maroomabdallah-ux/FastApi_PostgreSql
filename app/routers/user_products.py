from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserProductCreate, MyProductResponse
from app.security import get_current_user, require_admin
from app.models import User
from app import crud

router = APIRouter(
    prefix="/user-products",
    tags=["User Products"]
)


@router.post("/", response_model=MyProductResponse)
def assign_product(
    user_product: UserProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return crud.assign_product_to_user(
        db,
        user_product
    )


@router.get("/my", response_model=list[MyProductResponse])
def my_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_user_products(
        db,
        current_user.id
    )




@router.get(
    "/{user_id}",
    response_model=list[MyProductResponse]
)
def user_products(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return crud.get_user_products(
        db,
        user_id
    )