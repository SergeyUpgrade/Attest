from sqlalchemy.ext.asyncio import AsyncSession
import services as ss
import schemas as sm

async def show_products(session: AsyncSession, is_admin: bool):
    if is_admin:
        products = await ss.get_products_for_admin(session=session)
    else:
        products = await ss.get_products_for_customer(session=session)
    items: list[sm.Product] = []
    for product in products:
        items.append(sm.Product(id=product.id, price=product.price, name=product.name))
    return sm.ProductList(items=items)


async def show_cart(session: AsyncSession, user_id: int):
    cart = await ss.get_or_create_cart(session=session, user_id=user_id)
    cart_products = await ss.get_cart_products(session=session, cart_id=cart.id)
    items: list[sm.Product] = []
    for cart_product in cart_products:
        items.append(sm.Product(id=cart_product.id, price=cart_product.price, name=cart_product.name))
    total_price = await ss.get_total_price_of_products(session=session, cart_id=cart.id)
    return sm.Cart(items=items, total_price=total_price)
