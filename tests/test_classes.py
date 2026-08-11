import pytest
from src.classes import Product, Category


def test_product_creation():
    """Тест корректной инициализации товара."""
    product = Product("Телефон", "Смартфон", 50000.0, 5)
    assert product.name == "Телефон"
    assert product.description == "Смартфон"
    assert product.price == 50000.0
    assert product.quantity == 5


def test_category_creation():
    """Тест корректной инициализации категории."""
    product1 = Product("Книга", "Учебник", 1000.0, 3)
    product2 = Product("Ручка", "Шариковая", 50.0, 20)
    category = Category("Канцтовары", "Товары для офиса", [product1, product2])

    assert category.name == "Канцтовары"
    assert category.description == "Товары для офиса"
    # Проверяем, что геттер возвращает строку
    assert isinstance(category.products, str)


def test_category_count_increment():
    """Тест автоматического увеличения счётчика категорий."""
    initial_count = Category.category_count
    category = Category("Тестовая категория", "Описание", [])
    assert Category.category_count == initial_count + 1


def test_product_count_increment():
    """Тест автоматического увеличения счётчика продуктов."""
    initial_count = Category.product_count
    product1 = Product("Товар 1", "Описание", 100.0, 2)
    product2 = Product("Товар 2", "Описание", 200.0, 3)
    category = Category("Категория", "Описание", [product1, product2])
    assert Category.product_count == initial_count + 2


# Новые тесты для задания 14.2

def test_add_product():
    """Тест метода add_product."""
    # Сохраняем начальное значение счётчика продуктов
    initial_count = Category.product_count
    
    category = Category("Тест", "Описание", [])
    product = Product("Новый товар", "Описание", 500.0, 10)
    category.add_product(product)
    
    # Проверяем, что счётчик увеличился на 1
    assert Category.product_count == initial_count + 1
    assert "Новый товар" in category.products

def test_product_price_setter_valid():
    """Тест сеттера цены с корректным значением."""
    product = Product("Товар", "Описание", 100.0, 5)
    product.price = 150.0
    assert product.price == 150.0


def test_product_price_setter_invalid():
    """Тест сеттера цены с некорректным значением."""
    product = Product("Товар", "Описание", 100.0, 5)
    product.price = -50.0  # Должно вывести сообщение и не изменить цену
    assert product.price == 100.0


def test_new_product_from_dict():
    """Тест класс-метода new_product."""
    product_data = {
        "name": "Ноутбук",
        "description": "Мощный ноутбук",
        "price": 80000.0,
        "quantity": 7
    }
    product = Product.new_product(product_data)
    assert product.name == "Ноутбук"
    assert product.price == 80000.0
    assert product.quantity == 7


def test_category_products_getter():
    """Тест геттера products в Category."""
    product = Product("Телефон", "Смартфон", 30000.0, 3)
    category = Category("Электроника", "Техника", [product])
    expected_output = "Телефон, 30000.0 руб. Остаток: 3 шт.\n"
    assert category.products == expected_output


# Новые тесты для задания 15.1

def test_product_str():
    """Тест строкового представления продукта."""
    product = Product("Ноутбук", "Мощный ноутбук", 150000.0, 10)
    expected = "Ноутбук, 150000.0 руб. Остаток: 10 шт."
    assert str(product) == expected


def test_category_str():
    """Тест строкового представления категории."""
    product1 = Product("Книга", "Учебник", 1000.0, 3)
    product2 = Product("Ручка", "Шариковая", 50.0, 20)
    category = Category("Канцтовары", "Товары для офиса", [product1, product2])
    expected = "Канцтовары, количество продуктов: 23 шт."
    assert str(category) == expected


def test_product_add():
    """Тест магического метода __add__."""
    product1 = Product("Товар 1", "Описание", 100.0, 10)
    product2 = Product("Товар 2", "Описание", 200.0, 2)
    result = product1 + product2
    assert result == 100 * 10 + 200 * 2  # 1400


def test_product_add_type_error():
    """Тест, что сложение с не-Product вызывает ошибку."""
    product = Product("Товар", "Описание", 100.0, 5)
    with pytest.raises(TypeError, match="Можно складывать только объекты Product"):
        _ = product + 10