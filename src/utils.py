import json
import os
from typing import Any

from src.Category import Category
from src.Product import Product


def read_json(path: str) -> Any:
    "Функция для считывая файла формата json"
    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="UTF-8") as file:
        product_info = json.load(file)
    return product_info


def create_objects_from_json(product_info: Any) -> Any:
    "Функция для создания объектов классов"
    categories = []
    all_products: list[Product] = []  # Собираем все продукты для проверки дубликатов
    for category_data in product_info:
        # Создаем список объектов Product для этой категории
        product_objects = []
        for product_dict in category_data["products"]:
            # Используем new_product с проверкой дубликатов
            product = Product.new_product(product_dict, all_products)
            product_objects.append(product)
            all_products.append(product)

        # Создаем объект Category
        category = Category(
            name=category_data["name"], description=category_data["description"], products=product_objects
        )
        categories.append(category)

    return categories
