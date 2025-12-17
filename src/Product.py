from typing import Any, Optional


class Product:
    "Класс для продуктов без атрибутов"

    name: str
    description: str
    __price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """Строковое представление продукта в формате: Название продукта, __руб. Остаток: __ шт."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> Any:
        """Сложение продуктов: сумма стоимости всех товаров на складе"""
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        # Полная стоимость = цена × количество
        total_self = self.price * self.quantity
        total_other = other.price * other.quantity
        return total_self + total_other

    @classmethod
    def new_product(cls, product_data: dict, products_list: Optional[list] = None) -> Any:
        """Класс-метод для создания нового продукта с проверкой дубликатов"""
        if products_list is None:
            products_list = []
        # Проверяем существующие товары на дубликаты
        for existing_product in products_list:
            if existing_product.name.lower() == product_data["name"].lower:
                # Объединяем количества
                existing_product.quantity += product_data.get("quantity", 0)
                # Выбираем максимальную цену
                existing_product.price = max(existing_product.price, product_data.get("price", 0))
                return existing_product
        # Если дубликат не найден, создаем новый товар
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    @property
    def price(self) -> Any:
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> Any:
        """Сеттер для цены с проверкой и подтверждением"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        # Если цена понижается, запрашиваем подтверждение
        if hasattr(self, "_Product__price") and new_price < self.__price:
            confirmation = input(f"Цена понижается с {self.__price} до {new_price}. Подтвердите изменение (y/n): ")
            if confirmation.lower() != "y":
                print("Изменение цены отменено")
                return

        self.__price = new_price
