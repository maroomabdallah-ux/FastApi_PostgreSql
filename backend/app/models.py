from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# ==========================
# User
# ==========================
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    google_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    password: Mapped[str] = mapped_column(String(255))

    role: Mapped[str] = mapped_column(
        String(20),
        default="USER"
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    user_products: Mapped[list["UserProduct"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ==========================
# Post
# ==========================
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(200))

    content: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(
        back_populates="posts"
    )


# ==========================
# Product
# ==========================
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    description: Mapped[str] = mapped_column(Text)

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    stock_quantity: Mapped[int] = mapped_column(default=0)

    user_products: Mapped[list["UserProduct"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )


# ==========================
# UserProduct
# ==========================
class UserProduct(Base):
    __tablename__ = "user_products"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE")
    )

    quantity: Mapped[int] = mapped_column(default=1)

    user: Mapped["User"] = relationship(
        back_populates="user_products"
    )

    product: Mapped["Product"] = relationship(
        back_populates="user_products"
    )
