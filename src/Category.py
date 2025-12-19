from abc import ABC, abstractmethod
from typing import Any

from src.Product import BaseProduct


class BaseContainer(ABC):
    """Абстрактный базовый класс для контейнеров с продуктами"""

    @abstractmethod
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление контейнера"""
        pass

    @property
    @abstractmethod
    def products(self) -> str:
        """Геттер для получения продуктов"""
        pass


class Category(BaseContainer):
    "Класс категорий продуктов"

    name: str
    description: str
    __products: list
    product_count = 0
    category_count = 0

    def __init__(self, name: str, description: str, products: Any) -> None:
        super().__init__(name, description)
        self.__products = products if products else []
        Category.product_count += len(self.__products)
        Category.category_count += 1

    def __str__(self) -> str:
        """Строковое представление категории в формате: Название категории, количество продуктов: 200 шт."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> Any:
        """Возвращает итератор для перебора продуктов в категории"""
        return CategoryIterator(self.__products)

    def add_product(self, new_product: Any) -> None:
        """Метод для добавления товара в категорию с проверкой типа"""
        # Проверяем, что new_product является BaseProduct или его наследником
        if not isinstance(new_product, BaseProduct):
            raise TypeError("Можно добавлять только объекты класса BaseProduct или его наследников")

        self.__products.append(new_product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер для получения строкового представления товаров"""
        products_info = []
        for product in self.__products:
            products_info.append(str(product))
        return "\n".join(products_info)


class CategoryIterator:
    """Вспомогательный класс для итерации по товарам категории"""

    def __init__(self, products: list) -> None:
        self.products = products
        self.index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> Any:
        """Возвращает очередной товар категории"""
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        raise StopIteration


class Order(BaseContainer):
    """Класс для заказов"""

    def __init__(self, product: BaseProduct, quantity: int) -> None:
        super().__init__(f"Заказ для {product.name}", f"Заказ продукта {product.name}")
        self.product = product
        self.order_quantity = quantity
        self.total_price = product.price * quantity

    def __str__(self) -> str:
        """Строковое представление заказа"""
        return (
            f"Заказ: {self.product.name}, "
            f"Количество: {self.order_quantity}, "
            f"Итоговая стоимость: {self.total_price} руб."
        )

    @property
    def products(self) -> str:
        """Геттер для получения продуктов в заказе"""
        return f"{self.product.name} - {self.order_quantity} шт."
