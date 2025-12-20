from typing import Any
from unittest.mock import patch

import pytest

from src.Category import Category, Order
from src.Product import BaseProduct, LawnGrass, Product, Smartphone, ZeroQuantityError


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


def test_smartphone_initialization() -> None:
    """Тест инициализации Smartphone"""
    smartphone = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый")

    assert smartphone.name == "Samsung Galaxy S23 Ultra"
    assert smartphone.price == 180000.0
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23 Ultra"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"
    assert isinstance(smartphone, Product)
    assert isinstance(smartphone, Smartphone)


def test_lawn_grass_initialization() -> None:
    """Тест инициализации LawnGrass"""
    grass = LawnGrass("Газонная трава", "Элитная трава", 500.0, 20, "Россия", "7 дней", "Зеленый")

    assert grass.name == "Газонная трава"
    assert grass.price == 500.0
    assert grass.quantity == 20
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"
    assert isinstance(grass, Product)
    assert isinstance(grass, LawnGrass)


def test_add_same_class_products() -> None:
    """Тест сложения продуктов одного класса"""
    smartphone1 = Smartphone("Phone1", "Desc", 100.0, 5, 90.0, "Model1", 128, "Black")
    smartphone2 = Smartphone("Phone2", "Desc", 200.0, 3, 95.0, "Model2", 256, "White")

    result = smartphone1 + smartphone2
    assert result == (100.0 * 5) + (200.0 * 3)  # 500 + 600 = 1100


def test_base_product_abstract_class() -> None:
    """Тест, что BaseProduct является абстрактным классом"""
    from abc import ABC

    assert issubclass(BaseProduct, ABC)

    # Проверяем, что Product наследует BaseProduct
    assert issubclass(Product, BaseProduct)
    assert issubclass(Smartphone, BaseProduct)
    assert issubclass(LawnGrass, BaseProduct)


def test_product_repr() -> None:
    """Тест метода __repr__"""
    product = Product("Продукт", "Описание", 150.0, 10)

    repr_str = repr(product)
    assert "Product('Продукт', 'Описание', 150.0, 10)" == repr_str

    smartphone = Smartphone("Phone", "Smartphone", 300.0, 5, 90.0, "S10", 128, "White")
    repr_str = repr(smartphone)
    assert "Smartphone('Phone', 'Smartphone', 300.0, 5, 90.0, 'S10', 128, 'White')" in repr_str


def test_order_class() -> None:
    """Тест класса Order"""
    product = Product("Товар", "Описание", 100.0, 50)
    order = Order(product, 5)

    assert order.name == f"Заказ для {product.name}"
    assert order.product == product
    assert order.order_quantity == 5
    assert order.total_price == 100.0 * 5

    # Проверка строкового представления
    assert str(order) == "Заказ: Товар, Количество: 5, Итоговая стоимость: 500.0 руб."

    # Проверка геттера products
    assert order.products == "Товар - 5 шт."


def test_order_with_different_products() -> None:
    """Тест Order с разными типами продуктов"""
    smartphone = Smartphone("Phone", "Smart", 200.0, 10, 95.0, "M1", 256, "Black")
    smartphone_order = Order(smartphone, 2)

    assert smartphone_order.total_price == 400.0
    assert "Phone" in str(smartphone_order)

    grass = LawnGrass("Трава", "Газонная", 50.0, 100, "Россия", "7 дней", "Зеленый")
    grass_order = Order(grass, 10)

    assert grass_order.total_price == 500.0
    assert "Трава" in str(grass_order)


def test_base_container_abstract_class() -> None:
    """Тест, что BaseContainer является абстрактным классом"""
    from abc import ABC

    from src.Category import BaseContainer, Category

    assert issubclass(BaseContainer, ABC)
    assert issubclass(Category, BaseContainer)
    assert issubclass(Order, BaseContainer)

    # Проверяем общие свойства
    category = Category("Категория", "Описание", [])
    order = Order(Product("Товар", "Оп", 100.0, 10), 2)

    assert hasattr(category, "name")
    assert hasattr(category, "description")
    assert hasattr(category, "products")

    assert hasattr(order, "name")
    assert hasattr(order, "description")
    assert hasattr(order, "products")


def test_product_zero_quantity() -> None:
    """Тест создания продукта с нулевым количеством"""
    # Проверяем, что создание продукта с нулевым количеством вызывает ValueError
    with pytest.raises(ValueError) as exc_info:
        Product("Бракованный товар", "Неверное количество", 1000.0, 0)

    assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)

    # Проверяем, что создание продукта с положительным количеством работает
    product = Product("Нормальный товар", "Описание", 1000.0, 5)
    assert product.quantity == 5


def test_smartphone_zero_quantity() -> None:
    """Тест создания смартфона с нулевым количеством"""
    with pytest.raises(ValueError) as exc_info:
        Smartphone("Бракованный телефон", "Описание", 50000.0, 0, 95.0, "ModelX", 256, "Black")

    assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)


def test_lawn_grass_zero_quantity() -> None:
    """Тест создания травы с нулевым количеством"""
    with pytest.raises(ValueError) as exc_info:
        LawnGrass("Бракованная трава", "Описание", 500.0, 0, "Россия", "7 дней", "Зеленый")

    assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)


def test_category_middle_price() -> None:
    """Тест метода middle_price для категории"""
    product1 = Product("Товар1", "Описание", 100.0, 5)
    product2 = Product("Товар2", "Описание", 200.0, 3)
    product3 = Product("Товар3", "Описание", 300.0, 2)

    category = Category("Категория", "Описание", [product1, product2, product3])

    # Средняя цена: (100 + 200 + 300) / 3 = 200.0
    assert category.middle_price() == 200.0


def test_category_middle_price_empty() -> None:
    """Тест метода middle_price для пустой категории"""
    category = Category("Пустая категория", "Описание", [])

    # Для пустой категории должно возвращаться 0
    assert category.middle_price() == 0.0


def test_category_middle_price_single_product() -> None:
    """Тест метода middle_price для категории с одним товаром"""
    product = Product("Товар", "Описание", 150.0, 10)
    category = Category("Категория", "Описание", [product])

    assert category.middle_price() == 150.0


def test_zero_quantity_error_class() -> None:
    """Тест пользовательского исключения ZeroQuantityError"""
    # Проверяем, что это исключение
    assert issubclass(ZeroQuantityError, Exception)

    # Проверяем создание исключения
    error = ZeroQuantityError("Тестовое сообщение")
    assert str(error) == "Тестовое сообщение"


def test_category_with_zero_quantity_product() -> None:
    """Тест создания категории с товаром нулевого количества"""
    product1 = Product("Товар1", "Описание", 100.0, 5)

    # Создаем товар с нулевым количеством напрямую (минуя проверку в конструкторе)
    class BadProduct(Product):
        def __init__(self, name: str, description: str, price: float, quantity: int):
            # Пропускаем проверку родительского класса
            self.name = name
            self.description = description
            self._Product__price = price
            self.quantity = quantity

    bad_product = BadProduct("Бракованный", "Описание", 50.0, 0)

    # Теперь проверяем, что категория не принимает такой товар
    with pytest.raises(ZeroQuantityError) as exc_info:
        Category("Категория", "Описание", [product1, bad_product])

    assert "имеет нулевое количество" in str(exc_info.value)


def test_add_product_with_zero_quantity() -> None:
    """Тест добавления товара с нулевым количеством в категорию"""
    product1 = Product("Товар1", "Описание", 100.0, 5)
    category = Category("Категория", "Описание", [product1])

    # Создаем товар с нулевым количеством (другой способ)
    class BadProduct2(Product):
        def __init__(self, name: str, description: str, price: float, quantity: int):
            # Пропускаем проверку родительского класса
            self.name = name
            self.description = description
            self._Product__price = price
            self.quantity = quantity

    bad_product = BadProduct2("Бракованный2", "Описание", 50.0, 0)

    # Пытаемся добавить товар с нулевым количеством
    with pytest.raises(ZeroQuantityError) as exc_info:
        category.add_product(bad_product)

    assert "имеет нулевое количество" in str(exc_info.value)


def test_order_with_zero_quantity_product() -> None:
    """Тест создания заказа с товаром нулевого количества"""

    # Создаем товар с нулевым количеством (обходным путем)
    class BadProduct3(Product):
        def __init__(self, name: str, description: str, price: float, quantity: int):
            self.name = name
            self.description = description
            self._Product__price = price
            self.quantity = quantity

    bad_product = BadProduct3("Товар без запаса", "Описание", 100.0, 0)

    # Пытаемся создать заказ
    with pytest.raises(ZeroQuantityError) as exc_info:
        Order(bad_product, 2)

    assert "имеет нулевое количество" in str(exc_info.value)


def test_add_product_success() -> None:
    """Тест успешного добавления товара в категорию"""
    product1 = Product("Товар1", "Описание", 100.0, 5)
    product2 = Product("Товар2", "Описание", 200.0, 3)

    category = Category("Категория", "Описание", [product1])

    initial_count = len(category.products.split("\n")) if category.products else 0

    # Успешное добавление
    category.add_product(product2)

    # Проверяем, что товар добавлен
    final_count = len(category.products.split("\n")) if category.products else 0
    assert final_count == initial_count + 1
    assert "Товар2" in category.products


def test_new_product_with_zero_quantity() -> None:
    """Тест new_product с нулевым количеством"""
    product_data = {"name": "Товар", "description": "Описание", "price": 100.0, "quantity": 0}

    with pytest.raises(ValueError) as exc_info:
        Product.new_product(product_data)

    assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)


def test_regular_product_creation() -> None:
    """Тест, что обычные товары создаются нормально"""
    product = Product("Нормальный товар", "Описание", 100.0, 10)
    assert product.name == "Нормальный товар"
    assert product.quantity == 10
    assert product.price == 100.0

    smartphone = Smartphone("Смартфон", "Описание", 200.0, 5, 95.0, "ModelX", 256, "Black")
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 95.0
