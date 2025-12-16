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
        self.__products = products
        Category.product_count += len(products) if products else 0
        Category.category_count += 1

    def add_product(self, new_product: Product) -> Any:
        """Метод для добавления товара в категорию"""
        self.__products.append(new_product)
        Category.product_count += 1

    @property
    def products(self) -> Any:
        """Геттер для получения строкового представления товаров"""
        products_info = []
        for product in self.__products:
            products_info.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")
        return "\n".join(products_info)
