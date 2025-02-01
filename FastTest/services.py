from passlib.context import CryptContext
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Product, Cart, CartItem

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def __get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(session: AsyncSession, name: str, phone_number: str, email: str, is_admin: bool, password: str):
    user = User(
        name=name,
        phone_number=phone_number,
        email=email,
        is_admin=is_admin,
        password=__get_password_hash(password)
    )
    session.add(user)
    await session.flush()
    return user.id


async def login_user(session: AsyncSession, phone_number: str, email: str, password: str) -> User | None:
    if phone_number:
        result = await session.scalars(select(User).filter(User.phone_number == phone_number))
    elif email:
        result = await session.scalars(select(User).filter(User.email == email))
    else:
        raise ValueError('Укажите телефон или емейл пользователя')
    user = result.one_or_none()
    if user is None:
        return None
    if not pwd_context.verify(password, user.password):
        return None
    return user


async def get_user_role(session: AsyncSession, user_id: int):
    user = await get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise ValueError(f'Пользователя {user_id} не существует')
    if user.is_admin:
        return 'admin'
    return 'customer'


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.scalars(select(User).filter(User.id == user_id))
    return result.one_or_none()


async def change_user_name(session: AsyncSession, user_id: int, new_name: str) -> None:
    #user = await get_user_by_id(session=session, user_id=user_id)
    #if user is None:
    #    raise ValueError(f"Пользователь с индентификатором {user_id} не найден")
    #print(type(user))
    #user.name = new_name
    #await session.flush()
    await session.execute(update(User).filter(User.id == user_id).values(name=new_name))
    await session.flush()


async def delete_user(session: AsyncSession, user_id: int) -> None:
    user = await get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise ValueError(f"Пользователь с индентификатором {user_id} не найден")
    await session.delete(user)
    await session.flush()


async def create_product(session: AsyncSession, name: str, price: float, is_active: bool):
    product = Product(name=name, price=price, is_active=is_active)
    session.add(product)
    await session.flush()
    return product.id


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    result = await session.scalars(select(Product).filter(Product.id == product_id))
    return result.one_or_none()


async def delete_product(session: AsyncSession, product_id: int) -> None:
    product = await get_product_by_id(session=session, product_id=product_id)
    if product is None:
        raise ValueError(f"Продукт с индентификатором {product_id} не найден")
    await session.delete(product)
    await session.flush()


async def change_product_activation(session: AsyncSession, product_id: int, is_active: bool) -> None:
    await session.execute(update(Product).filter(Product.id == product_id).values(is_active=is_active))
    await session.flush()


async def get_products_for_admin(session: AsyncSession) -> list[Product]:
    result = await session.scalars(select(Product))
    products = result.all()
    return list(products)


async def get_products_for_customer(session: AsyncSession) -> list[Product]:
    result = await session.scalars(select(Product).filter(Product.is_active==True))
    products = result.all()
    return list(products)


async def create_cart(session: AsyncSession, user_id: int):
    print(f"Создание корзины для пользователяч {user_id}")
    cart = Cart(user_id=user_id)
    session.add(cart)
    await session.flush()
    print(f"Корзина c id {cart.id} для пользователя {user_id} создана")
    return cart


async def get_cart_by_user_id(session: AsyncSession, user_id: int) -> Cart | None:
    result = await session.scalars(select(Cart).filter(Cart.user_id == user_id))
    return result.one_or_none()


async def get_or_create_cart(session: AsyncSession, user_id: int):
    cart = await get_cart_by_user_id(session=session, user_id=user_id)
    if cart is None:
        print(f'Корзины для пользователя с {user_id} еще нет')
        cart = await create_cart(session=session, user_id=user_id)
    else:
        print(f'Корзина для пользователя с {user_id} уже существует')
    return cart


async def create_cart_item(session: AsyncSession, cart_id: int, product_id: int):
    product = await get_product_by_id(session=session, product_id=product_id)
    if product is None:
        raise ValueError(f'Продукта {product_id} не существует')
    result = await session.scalars(select(CartItem).filter(CartItem.product_id == product_id, CartItem.cart_id == cart_id))
    if result.one_or_none() is not None:
        raise ValueError(f'Продукт {product_id} уже есть в корзине {cart_id}')
    if not product.is_active:
        raise ValueError(f'Продукта {product_id} неактивен')
    cart_item = CartItem(cart_id=cart_id, product_id=product_id)
    session.add(cart_item)
    await session.flush()
    return cart_item


async def get_cart_products(session: AsyncSession, cart_id: int) -> list[Product]:
    result = await session.scalars(select(CartItem).filter(CartItem.cart_id == cart_id))
    cart_items = result.all()
    products: list[Product] = []
    for cart_item in cart_items:
        product = await get_product_by_id(session=session, product_id=cart_item.product_id)
        products.append(product)
    return products

async def get_total_price_of_products(session: AsyncSession, cart_id: int) -> float:
    cart_products = await get_cart_products(session=session, cart_id=cart_id)
    total_price = 0
    for cart_product in cart_products:
        total_price += cart_product.price
    return total_price


async def delete_product_from_cart(session: AsyncSession, product_id: int, cart_id: int) -> None:
    await session.execute(delete(CartItem).filter(CartItem.cart_id == cart_id, CartItem.product_id == product_id))
    await session.flush()


async def delete_all_products_from_cart(session: AsyncSession, cart_id: int) -> None:
    await session.execute(delete(CartItem).filter(CartItem.cart_id == cart_id))
    await session.flush()
