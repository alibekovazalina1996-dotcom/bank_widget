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
    assert len(category.products) == 2
    assert category.products[0].name == "Книга"

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