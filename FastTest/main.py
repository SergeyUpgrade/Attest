import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session, db_create_tables
import services as s
import schemas as sm
import presentations as p


async def create_admin_user(session: AsyncSession):
    user_registration_sm = sm.UserRegistration(
        name='admin',
        phone_number='+79113899891',
        email='admin@admin.ru',
        password='Davakin12!',
        re_password='Davakin12!'
    )
    user_id = await s.create_user(
        name=user_registration_sm.name,
        phone_number=user_registration_sm.phone_number,
        email=user_registration_sm.email,
        password=user_registration_sm.password,
        is_admin=True,
        session=session
    )
    print(f'Создан админ с идентификатором {user_id}')
    return user_id


async def create_customer_user(session: AsyncSession):
    user_registration_sm = sm.UserRegistration(
        name='customer',
        phone_number='+79113899892',
        email='customer@customer.ru',
        password='Davakin12!',
        re_password='Davakin12!',
    )
    user_id = await s.create_user(
        name=user_registration_sm.name,
        phone_number=user_registration_sm.phone_number,
        email=user_registration_sm.email,
        password=user_registration_sm.password,
        is_admin=False,
        session=session
    )
    print(f'Создан покупатель с идентификатором {user_id}')
    return user_id


async def check_user_role(session: AsyncSession, user_id: int):
    role = await s.get_user_role(session=session, user_id=user_id)
    print(f"Роль пользователя {role}")


async def login_user(session: AsyncSession, phone_number: str, email: str, password: str):
    user = await s.login_user(session=session, phone_number=phone_number, email=email, password=password)
    if user is None:
        print(f'Пользователь не залогинен')
    else:
        print(f"Пользователь залогинен {user.password}")


async def test_user_by_id(session: AsyncSession, user_id: int):
    user = await s.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        print(f'Пользователь с идентификатором {user_id} не найден')
    else:
        print(f'Пользователь с идентификатором {user_id} найден')


async def change_customer_name(session: AsyncSession, user_id: int):
    await s.change_user_name(session, user_id=user_id, new_name='name1')
    customer = await s.get_user_by_id(session=session, user_id=user_id)
    if customer.name == 'name1':
        print('Имя изменено')


async def delete_customer(session: AsyncSession, user_id: int):
    await s.delete_user(session, user_id=user_id)
    print(f'Покупатель удален {user_id}')


async def create_product_milk(session: AsyncSession):
    new_product_sm = sm.NewProduct(name='Молоко', price=0.1)
    product_id = await s.create_product(name=new_product_sm.name, price=new_product_sm.price, is_active=True, session=session)
    print(f'Добавлено молоко {product_id}')
    return product_id


async def create_product_kefir(session: AsyncSession):
    new_product_sm = sm.NewProduct(name='Кефир', price=79.50)
    product_id = await s.create_product(name=new_product_sm.name, price=new_product_sm.price, is_active=True, session=session)
    print(f'Добавлен кефир {product_id}')
    return product_id


async def create_product_bananas(session: AsyncSession):
    new_product_sm = sm.NewProduct(name='Бананы', price=0.2)
    product_id = await s.create_product(name=new_product_sm.name, price=new_product_sm.price, is_active=True, session=session)
    print(f'Добавлены бананы {product_id}')
    return product_id


async def test_product_by_id(session: AsyncSession, product_id: int):
    product = await s.get_product_by_id(session=session, product_id=product_id)
    if product is None:
        print(f'Продукт с идентификатором {product_id} не найден')
    else:
        print(f'Продукт с идентификатором {product_id} найден')


async def delete_product(session: AsyncSession, product_id: int):
    await s.delete_product(session, product_id=product_id)
    print(f'Продукт удален {product_id}')


async def activate_product(session: AsyncSession, product_id: int):
    await s.change_product_activation(session, product_id=product_id, is_active=True)
    print(f'Активация продукта {product_id}')


async def deactivate_product(session: AsyncSession, product_id: int):
    await s.change_product_activation(session, product_id=product_id, is_active=False)
    print(f'Деактивация продукта {product_id}')


async def test_product_activation(session: AsyncSession, product_id: int):
    product = await s.get_product_by_id(session=session, product_id=product_id)
    if product.is_active:
        print(f'Продукт с идентификатором {product_id} активен')
    else:
        print(f'Продукт с идентификатором {product_id} неактивен')


async def get_products_for_admin(session: AsyncSession):
    print("Продукты админа:")
    products = await s.get_products_for_admin(session)
    for product in products:
        print(f"- Продукт №{product.id}: {product.name}")
    return products


async def get_products_for_customer(session: AsyncSession):
    print("Продукты покупателя:")
    products = await s.get_products_for_customer(session)
    for product in products:
        print(f"- Продукт №{product.id}: {product.name}")
    return products


async def get_customer_cart(session: AsyncSession, user_id: int):
    cart = await s.get_or_create_cart(session=session, user_id=user_id)
    print(f'Получена корзина {cart.id} для пользователя {user_id}')
    return cart


async def add_product_to_cart(session: AsyncSession, cart_id: int, product_id: int):
    cart_item_id = await s.create_cart_item(session=session, cart_id=cart_id, product_id=product_id)
    print(f'В корзину {cart_id} добавлен продукт {product_id}')
    return cart_item_id


async def get_cart_products(session: AsyncSession, cart_id: int):
    cart_products = await s.get_cart_products(session=session, cart_id=cart_id)
    print(f"В корзине {cart_id} находятся:")
    for cart_product in cart_products:
        print(cart_product.name)
    return cart_products


async def get_total_price_of_products_in_cart(session: AsyncSession, cart_id: int):
    total_price = await s.get_total_price_of_products(session=session, cart_id=cart_id)
    print(f"Сумма товаров в корзине {cart_id}: {total_price}")


async def delete_product_from_cart(session: AsyncSession, cart_id: int, product_id: int):
    await s.delete_product_from_cart(session=session, cart_id=cart_id, product_id=product_id)
    print(f"Продукт {product_id} удален из корзины {cart_id}")


async def clear_cart(session: AsyncSession, cart_id: int):
    await s.delete_all_products_from_cart(session=session, cart_id=cart_id)
    print(f"Корзина {cart_id} очищена")

async def products_endpoint(session: AsyncSession):
    response = await p.show_products(session=session, is_admin=True)
    print(response)

async def cart_endpoint(session: AsyncSession, user_id: int):
    response = await p.show_cart(session=session, user_id=user_id)
    print(response)

async def main():
    await db_create_tables()
    session = await get_session()
    admin_user_id = await create_admin_user(session)
    await test_user_by_id(session, user_id=admin_user_id)
    customer_user_id = await create_customer_user(session)
    await test_user_by_id(session, user_id=customer_user_id)
    await change_customer_name(session, user_id=customer_user_id)
    await login_user(session, phone_number='admin', email='', password='1234567')
    await login_user(session, phone_number='', email='customer', password='123456')

    customer_user_id_1 = await create_customer_user(session)
    await delete_customer(session, user_id=customer_user_id_1)
    await test_user_by_id(session, user_id=customer_user_id_1)
    await check_user_role(session, user_id=admin_user_id)
    await check_user_role(session, user_id=customer_user_id)

    milk_id = await create_product_milk(session)
    await test_product_by_id(session, product_id=milk_id)
    await deactivate_product(session, product_id=milk_id)
    await test_product_activation(session, product_id=milk_id)
    await activate_product(session, product_id=milk_id)
    await test_product_activation(session, product_id=milk_id)
    kefir_id = await create_product_kefir(session)
    await delete_product(session, product_id=kefir_id)
    await test_product_by_id(session, product_id=kefir_id)

    banan_id = await create_product_bananas(session)
    #await deactivate_product(session, product_id=banan_id)
    await get_products_for_admin(session)
    await get_products_for_customer(session)

    await get_customer_cart(session, user_id=customer_user_id)
    await get_customer_cart(session, user_id=customer_user_id)

    cart = await get_customer_cart(session, user_id=customer_user_id)
    await add_product_to_cart(session, cart_id=cart.id, product_id=banan_id)
    await add_product_to_cart(session, cart_id=cart.id, product_id=milk_id)

    await get_cart_products(session, cart_id=cart.id)
    await get_total_price_of_products_in_cart(session, cart_id=cart.id)

    #await delete_product_from_cart(session, cart_id=cart.id, product_id=milk_id)
    #await get_cart_products(session, cart_id=cart.id)

    #await clear_cart(session, cart_id=cart.id)
    #await get_cart_products(session, cart_id=cart.id)

    await products_endpoint(session)
    await cart_endpoint(session, customer_user_id)

    await session.commit()
    await session.close()


if __name__ == "__main__":
    asyncio.run(main())
