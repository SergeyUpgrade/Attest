
from sqlalchemy import text, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    is_admin: Mapped[bool] = mapped_column(
        default=False,
        server_default=text('false'),
        nullable=False
    )


class Product(Base):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float] = mapped_column(Float(asdecimal=True))
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=text('false'),
        nullable=False
    )

class Cart(Base):
    __tablename__ = 'cart'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
    )

class CartItem(Base):
    __tablename__ = 'cart_item'
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cart.id"),
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("product.id"),
    )
