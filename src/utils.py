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
    for category_data in product_info:
        # Создаем список объектов Product для этой категории
        product_objects = []
        for product_dict in category_data["products"]:
            product_objects.append(Product(**product_dict))

        # Создаем объект Category
        category = Category(
            name=category_data["name"], description=category_data["description"], products=product_objects
        )
        categories.append(category)

    return categories
