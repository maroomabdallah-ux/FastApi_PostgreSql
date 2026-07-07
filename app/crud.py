from sqlalchemy.orm import Session

from app.models import User, Post
from app.schemas import UserCreate, UserUpdate, PostCreate, PostUpdate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email
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