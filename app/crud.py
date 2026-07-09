from sqlalchemy.orm import Session
from app.security import hash_password
from app.security import verify_password
from app.models import User, Post, Product, UserProduct
from app.schemas import UserCreate, UserUpdate, PostCreate, PostUpdate
from app.schemas import ProductCreate, UserProductCreate
def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role="USER"
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_all_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)

    if not db_user:
        return None

    db_user.name = user.name
    db_user.email = user.email

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)

    if user:
        db.delete(user)
        db.commit()

    return user

################################
def create_post(db: Session, post: PostCreate):
    db_post = Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def get_all_posts(db: Session):
    return db.query(Post).all()


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def update_post(db: Session, post_id: int, post: PostUpdate):
    db_post = get_post(db, post_id)

    if not db_post:
        return None

    db_post.title = post.title
    db_post.content = post.content

    db.commit()
    db.refresh(db_post)

    return db_post


def delete_post(db: Session, post_id: int):
    post = get_post(db, post_id)

    if post:
        db.delete(post)
        db.commit()

    return post


#####################################
def get_posts_by_user(db: Session, user_id: int):
    return db.query(Post).filter(
        Post.user_id == user_id
    ).all()

######################################
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(
        User.email == email
    ).first()
######################################
def authenticate_user(db: Session, email: str, password: str):

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


########################################
def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)

    if product:
        db.delete(product)
        db.commit()

    return product


def get_my_products(db: Session, user_id: int):
    return get_user_products(db, user_id)


########################################
def assign_product_to_user(
    db: Session,
    user_product: UserProductCreate
):

    assignment = UserProduct(
        user_id=user_product.user_id,
        product_id=user_product.product_id,
        quantity=user_product.quantity
    )

    db.add(assignment)

    db.commit()

    db.refresh(assignment)

    return assignment


def add_product_to_user(
    db: Session,
    user_id: int,
    product_id: int,
    quantity: int
):
    assignment = db.query(UserProduct).filter(
        UserProduct.user_id == user_id,
        UserProduct.product_id == product_id
    ).first()

    if assignment:
        assignment.quantity += quantity
    else:
        assignment = UserProduct(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(assignment)

    db.commit()
    db.refresh(assignment)

    return assignment


def user_product_to_response(user_product: UserProduct):
    return {
        "id": user_product.product.id,
        "name": user_product.product.name,
        "description": user_product.product.description,
        "price": user_product.product.price,
        "quantity": user_product.quantity
    }


def get_user_products(db: Session, user_id: int):

    assignments = db.query(UserProduct).filter(
        UserProduct.user_id == user_id
    ).all()

    result = []

    for item in assignments:

        result.append(user_product_to_response(item))

    return result
