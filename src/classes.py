class Product:
    """Базовый класс для представления товара."""
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product или его наследников")
        if type(self) != type(other):
            raise TypeError("Нельзя складывать товары из разных категорий")
        return (self.__price * self.quantity) + (other.__price * other.quantity)

    @classmethod
    def new_product(cls, product_data: dict) -> 'Product':
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


class Smartphone(Product):
    """Класс для смартфонов."""
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: str, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для газонной травы."""
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


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

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        if not self.__products:
            return "В категории нет товаров."
        result = ""
        for product in self.__products:
            result += str(product) + "\n"
        return result