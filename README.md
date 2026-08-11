# Bank Widget Project  
  
Виджет для отображения банковских операций.  
  
## Установка  
  
1. Клонируйте репозиторий:  
   ```bash  
   git clone https://github.com/alibekovazalina1996-dotcom/bank_widget.git  
   ```  
2. Перейдите в папку проекта:  
   ```bash  
   cd bank_widget  
   ```  
3. Установите зависимости с помощью Poetry:  
   ```bash  
   poetry install  
   ```  
  
## Использование  
  
### Маскировка карты и счета  
  
```python  
from src.masks import get_mask_card_number, get_mask_account  
  
print(get_mask_card_number("7000792289606361"))   # 7000 79** **** 6361  
print(get_mask_account("73654108430135874305"))   # **4305  
```  
  
### Виджет  
  
```python  
from src.widget import mask_account_card, get_date  
  
print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361  
print(mask_account_card("Счет 73654108430135874305"))       # Счет **4305  
print(get_date("2024-03-11T02:26:18.671407"))              # 11.03.2024  
```  
  
### Обработка данных  
  
```python  
from src.processing import filter_by_state, sort_by_date  
  
operations = [  
    {"id": 1, "state": "EXECUTED", "date": "2024-03-11"},  
    {"id": 2, "state": "CANCELED", "date": "2024-02-01"},  
]  
  
print(filter_by_state(operations, "EXECUTED"))  
print(sort_by_date(operations, descending=True))  
```  
  
## Генераторы для работы с транзакциями  
  
Модуль `src/generators.py` содержит три функции-генератора:  
  
### 1. `filter_by_currency(transactions, currency)`  
  
Фильтрует транзакции по заданной валюте. Возвращает итератор.  
  
**Пример:**  
```python  
from src.generators import filter_by_currency  
  
transactions = [  
    {"operationAmount": {"currency": {"code": "USD"}}},  
    {"operationAmount": {"currency": {"code": "EUR"}}},  
]  
  
for tx in filter_by_currency(transactions, "USD"):  
    print(tx)  
```  
  
### 2. `transaction_descriptions(transactions)`  
  
Генерирует описания транзакций по очереди.  
  
**Пример:**  
```python  
from src.generators import transaction_descriptions  
  
transactions = [  
    {"description": "Перевод другу"},  
    {"description": "Оплата услуг"},  
]  
  
for desc in transaction_descriptions(transactions):  
    print(desc)  
```  
  
### 3. `card_number_generator(start, stop)`  
  
Генерирует номера карт в формате `XXXX XXXX XXXX XXXX`.  
  
**Пример:**  
```python  
from src.generators import card_number_generator  
  
for card in card_number_generator(1, 5):  
    print(card)  
```  
  
## Поиск и подсчёт категорий  
  
Модуль `src/processing.py` содержит две функции для работы с транзакциями:  
  
### 1. `search_by_description(transactions, search_string)`  
  
Ищет транзакции, в описании которых встречается заданная строка (без учёта регистра). Использует библиотеку `re` для работы с регулярными выражениями.  
  
**Пример:**  
```python  
from src.processing import search_by_description  
  
transactions = [  
    {"description": "Перевод другу"},  
    {"description": "Оплата услуг"},  
    {"description": "Перевод на карту"}  
]  
  
result = search_by_description(transactions, "перевод")  
# Вернёт первые две транзакции  
```  
  
### 2. `count_operations_by_category(transactions, categories)`  
  
Подсчитывает количество операций в каждой из переданных категорий на основе поля `description`. Использует `Counter` из библиотеки `collections`.  
  
**Пример:**  
```python  
from src.processing import count_operations_by_category  
  
transactions = [  
    {"description": "Перевод другу"},  
    {"description": "Оплата услуг"},  
    {"description": "Перевод на карту"},  
    {"description": "Оплата товаров"}  
]  
  
categories = ["Перевод", "Оплата"]  
result = count_operations_by_category(transactions, categories)  
# Вернёт {'Перевод': 2, 'Оплата': 2}  
```  
  
## Тестирование  
  
Для запуска тестов выполните:  
  
```bash  
pytest tests/  
```  
  
Отчет о покрытии тестами находится в файле `coverage_report.txt` и папке `htmlcov/`.  
  
## Технологии  
  
- Python 3.9+  
- Poetry  
- Git  
- GitHub  
- pandas  
- openpyxl  
  
## Лицензия  
  
MIT  
  
## Классы для интернет-магазина  
  
Модуль `src/classes.py` содержит два класса:  
  
### `Product`  
Представляет товар с атрибутами: название, описание, цена, количество.  
  
### `Category`  
Представляет категорию товаров. Содержит атрибуты класса:  
- `category_count` — общее количество категорий  
- `product_count` — общее количество продуктов  
  
## Классы-наследники для домашнего задания 16.1  
  
В рамках задания были созданы два класса-наследника от `Product`:  
  
### `Smartphone`  
Класс для смартфонов. Добавлены атрибуты:  
* `efficiency` — производительность  
* `model` — модель  
* `memory` — объем встроенной памяти  
* `color` — цвет  
  
### `LawnGrass`  
Класс для газонной травы. Добавлены атрибуты:  
* `country` — страна-производитель  
* `germination_period` — срок прорастания  
* `color` — цвет  
  
### Ограничения  
* Сложение (`__add__`) работает только для товаров одного класса.  
* Метод `add_product` в `Category` принимает только объекты `Product` или его наследников.  
  
## Абстрактные классы и миксины (домашнее задание 16.2)  
  
В проекте реализованы:  
  
### Базовый абстрактный класс `BaseProduct`  
Родительский класс для `Product`. Определяет абстрактные методы:  
* `__str__`  
* `__add__`  
* `price` (геттер и сеттер)  
  
### Класс-миксин `LogMixin`  
Добавляет логирование создания объектов. При инициализации объекта в консоль выводится сообщение:  
