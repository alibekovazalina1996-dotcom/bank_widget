from src.classes import Product, Category, Smartphone, LawnGrass

def main():
    # Создаём продукты
    product1 = Product("Ноутбук", "Мощный ноутбук", 150000.0, 10)
    product2 = Product("Мышь", "Беспроводная мышь", 3000.0, 25)
    
    # Создаём смартфоны
    phone1 = Smartphone("iPhone 15", "Смартфон", 100000.0, 10,
                        "Высокая", "15 Pro", 256, "Серый")
    phone2 = Smartphone("Samsung S24", "Смартфон", 80000.0, 3,
                        "Высокая", "S24", 256, "Черный")
    
    # Создаём траву
    grass = LawnGrass("Трава", "Газонная трава", 500.0, 20,
                      "Россия", "7 дней", "Зеленый")
    
    # Создаём категории
    category1 = Category("Электроника", "Товары для компьютеров", [product1, product2])
    category2 = Category("Смартфоны", "Мобильные телефоны", [phone1, phone2])
    category3 = Category("Садоводство", "Товары для сада", [grass])
    
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего продуктов: {Category.product_count}")
    print(category1)
    print(category2)
    print(category3)
    
    # Проверка сложения
    print(f"Стоимость iPhone 15 + Samsung S24: {phone1 + phone2}")
    
    # Проверка add_product
    new_phone = Smartphone("Xiaomi 14", "Смартфон", 60000.0, 5,
                           "Высокая", "14", 256, "Синий")
    category2.add_product(new_phone)
    print(f"После добавления Xiaomi: {category2}")

if __name__ == "__main__":
    main()