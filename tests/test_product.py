from typing import Any

from src.Product import Product


def test_product_initialization(product_data: Any) -> None:
    """Тест корректности инициализации Product"""
    product = Product(**product_data)

    assert product.name == "Samsung Galaxy C23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_product_attributes() -> None:
    """Тест атрибутов Product"""
    product = Product("Xiaomi", "128GB", 50000.0, 10)

    assert product.name == "Xiaomi"
    assert product.description == "128GB"
    assert product.price == 50000.0
    assert product.quantity == 10
