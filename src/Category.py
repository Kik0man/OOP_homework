from typing import Any

from src.Product import Product


class Category:
    "Класс категорий с двумя атрибутами"

    name: str
    description: str
    __products: list
    product_count = 0
    category_count = 0

    def __init__(self, name: str, description: str, products: Any) -> None:
        self.name = name
        self.description = description
        self.__products = products if products else []
        Category.product_count += len(self.__products)
        Category.category_count += 1

    def __str__(self) -> str:
        """Строковое представление категории в формате: Название категории, количество продуктов: __ шт."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> Any:
        """Возвращает итератор для перебора продуктов в категории"""
        return CategoryIterator(self.__products)

    def add_product(self, new_product: Product) -> None:
        """Метод для добавления товара в категорию"""
        self.__products.append(new_product)
        Category.product_count += 1

    @property
    def products(self) -> Any:
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
