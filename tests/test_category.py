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

    # Теперь category.products возвращает строку, а не список
    products_info = category.products
    assert "Samsung Galaxy C23 Ultra" in products_info
    assert "Iphone 15" in products_info

    # Для получения списка объектов можно использовать метод, если он есть
    # или проверить счетчик продуктов
    assert Category.product_count == 2


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

    # Для пустой категории products должен возвращать пустую строку
    assert category.products == ""
    assert Category.product_count == 0
    assert Category.category_count == 1


# НОВЫЕ ТЕСТЫ ДЛЯ НОВОЙ ФУНКЦИОНАЛЬНОСТИ:


def test_private_products_attribute() -> None:
    """Тест приватности атрибута __products"""
    product = Product("P1", "Desc", 100.0, 1)
    category = Category("Test", "Desc", [product])

    # Проверяем, что нельзя напрямую получить доступ к __products
    try:
        _ = category.__products
        assert False, "Должно быть исключение AttributeError"
    except AttributeError:
        assert True


def test_add_product_method() -> None:
    """Тест метода add_product"""
    product1 = Product("P1", "Desc", 100.0, 1)
    product2 = Product("P2", "Desc", 200.0, 2)

    category = Category("Test", "Desc", [product1])
    initial_count = Category.product_count

    category.add_product(product2)

    # Проверяем, что продукт добавлен (через геттер)
    products_info = category.products
    assert "P2" in products_info
    assert "200.0 руб." in products_info

    # Проверяем счетчик продуктов
    assert Category.product_count == initial_count + 1


def test_category_iterator() -> None:
    """Тест итератора категории"""
    product1 = Product("Товар1", "Описание", 100.0, 1)
    product2 = Product("Товар2", "Описание", 200.0, 2)
    product3 = Product("Товар3", "Описание", 300.0, 3)

    category = Category("Категория", "Описание", [product1, product2, product3])

    # Проверяем итерацию
    products_from_iterator = []
    for product in category:
        products_from_iterator.append(product)

    assert len(products_from_iterator) == 3
    assert products_from_iterator[0].name == "Товар1"
    assert products_from_iterator[1].name == "Товар2"
    assert products_from_iterator[2].name == "Товар3"


def test_category_str_representation() -> None:
    """Тест строкового представления Category"""
    product1 = Product("Товар1", "Описание", 100.0, 5)
    product2 = Product("Товар2", "Описание", 200.0, 3)

    category = Category("Категория", "Описание", [product1, product2])

    expected_str = "Категория, количество продуктов: 8 шт."
    assert str(category) == expected_str
