class Product:
    """Класс для представления товара."""
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    # Задание 1: строковое представление продукта
    def __str__(self) -> str:
        """Возвращает строковое представление продукта."""
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    # Задание 2: магический метод сложения
    def __add__(self, other: 'Product') -> float:
        """Возвращает общую стоимость товаров на складе (цена * количество)."""
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")
        return (self.__price * self.quantity) + (other.__price * other.quantity)

    @classmethod
    def new_product(cls, product_data: dict) -> 'Product':
        """Создает объект Product из словаря с данными."""
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    @property
    def price(self) -> float:
        """Возвращает цену товара."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Устанавливает цену, проверяя, что она положительная."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


class Category:
    """Класс для представления категории товаров."""
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    # Задание 1: строковое представление категории
    def __str__(self) -> str:
        """Возвращает строковое представление категории с общим количеством товаров."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию и обновляет счетчик."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строку с описанием всех продуктов в категории."""
        if not self.__products:
            return "В категории нет товаров."
        result = ""
        for product in self.__products:
            result += str(product) + "\n"
        return result