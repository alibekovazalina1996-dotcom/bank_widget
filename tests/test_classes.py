import pytest
from src.classes import Product, Category, Smartphone, LawnGrass

# Новые тесты для задания 16.1

def test_smartphone_creation():
    """Тест создания смартфона."""
    phone = Smartphone("iPhone 15", "Смартфон", 100000.0, 10,
                       "Высокая", "15 Pro", 256, "Серый")
    assert phone.name == "iPhone 15"
    assert phone.price == 100000.0
    assert phone.efficiency == "Высокая"
    assert phone.model == "15 Pro"
    assert phone.memory == 256
    assert phone.color == "Серый"


def test_lawn_grass_creation():
    """Тест создания газонной травы."""
    grass = LawnGrass("Трава", "Газонная трава", 500.0, 20,
                      "Россия", "7 дней", "Зеленый")
    assert grass.name == "Трава"
    assert grass.price == 500.0
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"


def test_add_same_type_products():
    """Тест сложения товаров одного типа."""
    phone1 = Smartphone("iPhone 15", "Смартфон", 100000.0, 2,
                        "Высокая", "15 Pro", 256, "Серый")
    phone2 = Smartphone("Samsung S24", "Смартфон", 80000.0, 3,
                        "Высокая", "S24", 256, "Черный")
    result = phone1 + phone2
    assert result == 100000 * 2 + 80000 * 3  # 200000 + 240000 = 440000


def test_add_different_type_products():
    """Тест сложения товаров разных типов (должна быть ошибка)."""
    phone = Smartphone("iPhone 15", "Смартфон", 100000.0, 2,
                       "Высокая", "15 Pro", 256, "Серый")
    grass = LawnGrass("Трава", "Газонная трава", 500.0, 20,
                      "Россия", "7 дней", "Зеленый")
    with pytest.raises(TypeError, match="Нельзя складывать товары из разных категорий"):
        _ = phone + grass


def test_add_product_to_category():
    """Тест добавления продукта в категорию с проверкой типа."""
    category = Category("Тест", "Описание", [])
    product = Product("Товар", "Описание", 100.0, 5)
    category.add_product(product)
    assert "Товар" in category.products

    # Проверка, что нельзя добавить не-Product
    with pytest.raises(TypeError, match="Можно добавлять только объекты Product или его наследников"):
        category.add_product("не_товар")

# ==================== НОВЫЕ ТЕСТЫ ДЛЯ 17.1 ====================

def test_product_zero_quantity():
    """Тест, что при создании продукта с нулевым количеством выбрасывается ошибка."""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Товар", "Описание", 100.0, 0)


def test_average_price_empty_category():
    """Тест средней цены для пустой категории."""
    category = Category("Пустая", "Описание", [])
    assert category.average_price() == 0.0


def test_average_price_non_empty_category():
    """Тест средней цены для категории с товарами."""
    product1 = Product("Товар 1", "Описание", 100.0, 5)
    product2 = Product("Товар 2", "Описание", 200.0, 3)
    category = Category("Категория", "Описание", [product1, product2])
    assert category.average_price() == 150.0