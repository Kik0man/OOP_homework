from abc import ABC, abstractmethod
from typing import Optional, Any


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов"""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление продукта"""
        pass

    @abstractmethod
    def __add__(self, other: "BaseProduct") -> float:
        """Сложение продуктов"""
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        """Геттер для цены"""
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float) -> None:
        """Сеттер для цены"""
        pass


class LoggingMixin:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        class_name = self.__class__.__name__
        # Формируем строку с параметрами
        params = []
        if hasattr(self, "name"):
            params.append(f"'{self.name}'")
        if hasattr(self, "description"):
            params.append(f"'{self.description}'")
        if hasattr(self, "price"):
            params.append(str(self.price))
        if hasattr(self, "quantity"):
            params.append(str(self.quantity))

        print(f"{class_name}({', '.join(params)})")


class Product(LoggingMixin, BaseProduct):
    "Класс для продуктов без атрибутов"

    name: str
    description: str
    __price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        # сначала LoggingMixin, потом BaseProduct
        super().__init__(name, description, price, quantity)
        self.__price = price

    def __str__(self) -> str:
        """Строковое представление продукта в формате: Название продукта, __руб. Остаток: __ шт."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> float:
        """Сложение продуктов: сумма стоимости всех товаров на складе"""
        if not isinstance(other, BaseProduct):
            raise TypeError("Можно складывать только объекты класса BaseProduct")

        # Проверяем, что продукты одного типа
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать продукты разных классов")

        # Полная стоимость = цена × количество
        total_self = self.price * self.quantity
        total_other = other.price * other.quantity
        return total_self + total_other

    @classmethod
    def new_product(cls, product_data: dict, products_list: Optional[list] = None) -> Any:
        """Класс-метод для создания нового продукта с проверкой дубликатов"""
        if products_list is None:
            products_list = []

        # Проверяем существующие товары на дубликаты
        for existing_product in products_list:
            if existing_product.name.lower() == product_data["name"].lower():
                # Объединяем количества
                existing_product.quantity += product_data.get("quantity", 0)
                # Выбираем максимальную цену
                new_price = product_data.get("price", 0)
                if new_price > existing_product.price:
                    existing_product.price = new_price
                return existing_product

        # Если дубликат не найден, создаем новый товар
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=float(product_data["price"]),
            quantity=int(product_data["quantity"]),
        )

    @property
    def price(self) -> float:
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой и подтверждением"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Если цена понижается, запрашиваем подтверждение
        if hasattr(self, "_Product__price") and new_price < self.__price:
            confirmation = input(f"Цена понижается с {self.__price} до {new_price}. Подтвердите изменение (y/n): ")
            if confirmation.lower() != "y":
                print("Изменение цены отменено")
                return

        self.__price = new_price

    def __repr__(self) -> str:
        """Репрезентативное представление объекта"""
        return f"{self.__class__.__name__}('{self.name}', '{self.description}', {self.price}, {self.quantity})"


class Smartphone(Product):
    """Класс для смартфонов, наследник Product"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency  # производительность
        self.model = model  # модель
        self.memory = memory  # объем встроенной памяти
        self.color = color  # цвет

    def __repr__(self) -> str:
        """Репрезентативное представление объекта Smartphone"""
        return (
            f"{self.__class__.__name__}('{self.name}', '{self.description}', "
            f"{self.price}, {self.quantity}, {self.efficiency}, '{self.model}', "
            f"{self.memory}, '{self.color}')"
        )


class LawnGrass(Product):
    """Класс для травы газонной, наследник Product"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country  # страна-производитель
        self.germination_period = germination_period  # срок прорастания
        self.color = color  # цвет

    def __repr__(self) -> str:
        """Репрезентативное представление объекта LawnGrass"""
        return (
            f"{self.__class__.__name__}('{self.name}', '{self.description}', "
            f"{self.price}, {self.quantity}, '{self.country}', '{self.germination_period}', "
            f"'{self.color}')"
        )
