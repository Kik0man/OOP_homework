from typing import Any

from src.Category import Category
from src.utils import create_objects_from_json


def setup_function() -> None:
    """Сброс счетчиков перед каждым тестом"""
    Category.product_count = 0
    Category.category_count = 0


def test_create_objects_from_json(category_data: Any) -> None:
    """Тест создания объектов из JSON данных"""
    json_data = [category_data]
    categories = create_objects_from_json(json_data)

    assert len(categories) == 1
    assert categories[0].name == "Смартфоны"

    # Теперь products возвращает строку, проверяем содержимое
    products_info = categories[0].products
    assert "Samsung Galaxy C23 Ultra" in products_info
    assert "Iphone 15" in products_info

    # Проверяем подсчет продуктов
    assert Category.product_count == 2
    assert Category.category_count == 1


def test_create_objects_from_empty_json() -> None:
    """Тест создания объектов из пустого JSON"""
    categories = create_objects_from_json([])

    assert categories == []
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_create_objects_multiple_categories() -> None:
    """Тест создания объектов из нескольких категорий"""
    json_data = [
        {
            "name": "Смартфоны",
            "description": "Описание 1",
            "products": [
                {"name": "P1", "description": "Desc", "price": 100.0, "quantity": 1},
                {"name": "P2", "description": "Desc", "price": 200.0, "quantity": 2},
            ],
        },
        {
            "name": "Телевизоры",
            "description": "Описание 2",
            "products": [{"name": "TV1", "description": "Desc", "price": 500.0, "quantity": 3}],
        },
    ]

    categories = create_objects_from_json(json_data)

    assert len(categories) == 2
    assert Category.category_count == 2
    assert Category.product_count == 3
    assert categories[0].name == "Смартфоны"
    assert categories[1].name == "Телевизоры"
