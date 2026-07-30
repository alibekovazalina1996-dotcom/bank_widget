from src.classes import Category, Product

def main():
    # Создаем продукты
    product1 = Product("Ноутбук", "Мощный игровой ноутбук", 150000.0, 10)
    product2 = Product("Мышь", "Беспроводная мышь", 3000.0, 25)
    product3 = Product("Наушники", "Беспроводные наушники", 12000.0, 15)

    # Создаем категории
    category1 = Category("Электроника", "Товары для компьютеров", [product1, product2])
    category2 = Category("Аксессуары", "Гарнитуры и аксессуары", [product3])

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего продуктов: {Category.product_count}")

if __name__ == "__main__":
    main()