import re

from pydantic import BaseModel, Field, field_validator, EmailStr
from pydantic_core.core_schema import ValidationInfo


class UserRegistration(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с +7 и содержать 10 цифр")
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    re_password: str = Field(..., min_length=5, max_length=50, description="Повторите пароль")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+7\d{10}$', value):
            raise ValueError('Номер телефона должен начинаться с "+7" и содержать 10 цифр')
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Пароль должен содержать не менее 8 символов')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать хотя бы один символ верхнего регистра')
        if not re.search(r'[$%&!:.]', v):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ ($%&!:)')
        if not re.match(r'^[a-zA-Z0-9$%&!:.]*$', v):
            raise ValueError('Пароль должен содержать только латинские буквы, цифры и специальные символы ($%&!:)')
        return v

    @field_validator("re_password")
    @classmethod
    def passwords_match(cls, values: str, info: ValidationInfo) -> str:
        if "re_password" in info.data and values != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return values


class NewProduct(BaseModel):
    name: str = Field(..., max_length=50, description="Название товара")
    price: float = Field(..., description="Цена товара")


class Product(NewProduct):
    id: int
    name: str
    price: float


class ProductList(BaseModel):
    items: list[Product]

class Cart(BaseModel):
    items: list[Product]
    total_price: float
