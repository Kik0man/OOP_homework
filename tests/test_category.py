from typing import Any

from src.Category import Category
from src.Product import Product


def setup_function() -> None:
    """Сброс счетчиков перед каждым тестом"""
    Category.product_count = 0
    Category.category_count = 0


def test_category_initialization(category_data: Any) -> None:
    """Тест корректности инициализации Category"""
    products = [Product(**p) for p in category_data["products"]]
    category = Category(name=category_data["name"], description=category_data["description"], products=products)

    assert category.name == "Смартфоны"
    assert category.description == "Смартфоны, как средство не только коммуникации..."
    assert len(category.products) == 2
    assert isinstance(category.products[0], Product)


def test_product_count() -> None:
    """Тест подсчета количества продуктов"""
    product1 = Product("P1", "Desc", 100.0, 1)
    product2 = Product("P2", "Desc", 200.0, 2)
    product3 = Product("P3", "Desc", 300.0, 3)

    Category("Cat1", "Desc", [product1, product2])
    assert Category.product_count == 2

    Category("Cat2", "Desc", [product3])
    assert Category.product_count == 3


def test_empty_category() -> None:
    """Тест пустой категории"""
    category = Category("Empty", "No products", [])

    assert category.name == "Empty"
    assert category.products == []
    assert Category.product_count == 0
    assert Category.category_count == 1
