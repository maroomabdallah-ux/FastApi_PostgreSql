from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import MyProductCreate, UserProductCreate, MyProductResponse
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
    assignment = crud.assign_product_to_user(
        db,
        user_product
    )

    return crud.user_product_to_response(assignment)


@router.post("/my", response_model=MyProductResponse)
def add_my_product(
    user_product: MyProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = crud.get_product(db, user_product.product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if user_product.quantity < 1:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    assignment = crud.add_product_to_user(
        db,
        current_user.id,
        user_product.product_id,
        user_product.quantity
    )

    return crud.user_product_to_response(assignment)


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
