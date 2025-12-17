from typing import Any
from unittest.mock import patch

from src.Category import Category
from src.Product import Product


def test_product_initialization(product_data: Any) -> None:
    """Тест корректности инициализации Product"""
    product = Product(**product_data)

    assert product.name == "Samsung Galaxy C23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.0  # Теперь через геттер
    assert product.quantity == 5


def test_product_attributes() -> None:
    """Тест атрибутов Product"""
    product = Product("Xiaomi", "128GB", 50000.0, 10)

    assert product.name == "Xiaomi"
    assert product.description == "128GB"
    assert product.price == 50000.0  # Теперь через геттер
    assert product.quantity == 10


# НОВЫЕ ТЕСТЫ ДЛЯ НОВОЙ ФУНКЦИОНАЛЬНОСТИ:


def test_price_getter_setter() -> None:
    """Тест геттера и сеттера цены"""
    product = Product("Товар", "Описание", 100.0, 10)

    # Проверяем геттер
    assert product.price == 100.0

    # Проверяем сеттер с положительной ценой
    product.price = 150
    assert product.price == 150.0


def test_price_setter_negative(capfd: Any) -> None:
    """Тест сеттера с отрицательной ценой"""
    product = Product("Товар", "Описание", 100.0, 10)

    # Пытаемся установить отрицательную цену
    product.price = -50

    # Цена не должна измениться
    assert product.price == 100.0

    # Проверяем вывод сообщения об ошибке
    captured = capfd.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_new_product_class_method() -> None:
    """Тест класс-метода new_product"""
    product_data = {"name": "Телефон", "description": "Смартфон", "price": 30000.0, "quantity": 10}

    product = Product.new_product(product_data)

    assert product.name == "Телефон"
    assert product.description == "Смартфон"
    assert product.price == 30000.0
    assert product.quantity == 10
    assert isinstance(product, Product)


def test_price_decrease_with_confirmation() -> None:
    """Тест понижения цены с подтверждением"""
    product = Product("Товар", "Описание", 100.0, 10)

    # Мокаем input для симуляции подтверждения (y)
    with patch("builtins.input", return_value="y"):
        product.price = 80

    # Цена должна измениться
    assert product.price == 80.0


def test_product_str_representation() -> None:
    """Тест строкового представления Product"""
    product = Product("Телефон", "Смартфон", 30000.0, 10)

    expected_str = "Телефон, 30000.0 руб. Остаток: 10 шт."
    assert str(product) == expected_str


def test_product_addition() -> None:
    """Тест сложения продуктов"""
    product_a = Product("Товар A", "Описание", 100.0, 10)
    product_b = Product("Товар B", "Описание", 200.0, 2)

    result = product_a + product_b

    # Ожидаемый результат: 100×10 + 200×2 = 1000 + 400 = 1400
    assert result == 1400.0


def test_products_getter_optimization() -> None:
    """Тест оптимизированного геттера products"""
    product1 = Product("Товар1", "Описание", 100.0, 5)
    product2 = Product("Товар2", "Описание", 200.0, 3)

    category = Category("Категория", "Описание", [product1, product2])

    products_str = category.products

    # Проверяем, что используется строковое представление продукта
    assert "Товар1, 100.0 руб. Остаток: 5 шт." in products_str
    assert "Товар2, 200.0 руб. Остаток: 3 шт." in products_str
