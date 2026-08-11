class Product:  
    """Базовый класс для представления товара."""  
    def __init__(self, name: str, description: str, price: float, quantity: int):  
        self.name = name  
        self.description = description  
        self.__price = price  
        self.quantity = quantity  
  
    def __str__(self) - 
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."  
  
    def __add__(self, other: 'Product') - 
        if not isinstance(other, Product):  
            raise TypeError("Можно складывать только объекты Product или его наследников")  
        if type(self) != type(other):  
            raise TypeError("Нельзя складывать товары из разных категорий")  
        return (self.__price * self.quantity) + (other.__price * other.quantity)  
  
    @classmethod  
    def new_product(cls, product_data: dict) - 
        return cls(  
            name=product_data['name'],  
            description=product_data['description'],  
            price=product_data['price'],  
            quantity=product_data['quantity']  
        )  
  
    @property  
    def price(self) - 
        return self.__price  
  
    @price.setter  
    def price(self, new_price: float) - 
