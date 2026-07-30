\# Bank Widget Project



Виджет для отображения банковских операций.



\## Установка



1\. Клонируйте репозиторий:

&#x20;  ```bash

&#x20;  git clone https://github.com/alibekovazalina1996-dotcom/bank\_widget.git

&#x20;  ```

2\. Перейдите в папку проекта:

&#x20;  ```bash

&#x20;  cd bank\_widget

&#x20;  ```

3\. Установите зависимости с помощью Poetry:

&#x20;  ```bash

&#x20;  poetry install

&#x20;  ```



\## Использование



\### Маскировка карты и счета



```python

from src.masks import get\_mask\_card\_number, get\_mask\_account



print(get\_mask\_card\_number("7000792289606361"))   # 7000 79\*\* \*\*\*\* 6361

print(get\_mask\_account("73654108430135874305"))   # \*\*4305

```



\### Виджет



```python

from src.widget import mask\_account\_card, get\_date



print(mask\_account\_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79\*\* \*\*\*\* 6361

print(mask\_account\_card("Счет 73654108430135874305"))       # Счет \*\*4305

print(get\_date("2024-03-11T02:26:18.671407"))              # 11.03.2024

```



\### Обработка данных



```python

from src.processing import filter\_by\_state, sort\_by\_date



operations = \[

&#x20;   {"id": 1, "state": "EXECUTED", "date": "2024-03-11"},

&#x20;   {"id": 2, "state": "CANCELED", "date": "2024-02-01"},

]



print(filter\_by\_state(operations, "EXECUTED"))

print(sort\_by\_date(operations, descending=True))

```



\## Генераторы для работы с транзакциями



Модуль `src/generators.py` содержит три функции-генератора:



\### 1. `filter\_by\_currency(transactions, currency)`



Фильтрует транзакции по заданной валюте. Возвращает итератор.



\*\*Пример:\*\*

```python

from src.generators import filter\_by\_currency



transactions = \[

&#x20;   {"operationAmount": {"currency": {"code": "USD"}}},

&#x20;   {"operationAmount": {"currency": {"code": "EUR"}}},

]



for tx in filter\_by\_currency(transactions, "USD"):

&#x20;   print(tx)

```



\### 2. `transaction\_descriptions(transactions)`



Генерирует описания транзакций по очереди.



\*\*Пример:\*\*

```python

from src.generators import transaction\_descriptions



transactions = \[

&#x20;   {"description": "Перевод другу"},

&#x20;   {"description": "Оплата услуг"},

]



for desc in transaction\_descriptions(transactions):

&#x20;   print(desc)

```



\### 3. `card\_number\_generator(start, stop)`



Генерирует номера карт в формате `XXXX XXXX XXXX XXXX`.



\*\*Пример:\*\*

```python

from src.generators import card\_number\_generator



for card in card\_number\_generator(1, 5):

&#x20;   print(card)

```



\## Поиск и подсчёт категорий



Модуль `src/processing.py` содержит две функции для работы с транзакциями:



\### 1. `search\_by\_description(transactions, search\_string)`



Ищет транзакции, в описании которых встречается заданная строка (без учёта регистра). Использует библиотеку `re` для работы с регулярными выражениями.



\*\*Пример:\*\*

```python

from src.processing import search\_by\_description



transactions = \[

&#x20;   {"description": "Перевод другу"},

&#x20;   {"description": "Оплата услуг"},

&#x20;   {"description": "Перевод на карту"}

]



result = search\_by\_description(transactions, "перевод")

\# Вернёт первые две транзакции

```



\### 2. `count\_operations\_by\_category(transactions, categories)`



Подсчитывает количество операций в каждой из переданных категорий на основе поля `description`. Использует `Counter` из библиотеки `collections`.



\*\*Пример:\*\*

```python

from src.processing import count\_operations\_by\_category



transactions = \[

&#x20;   {"description": "Перевод другу"},

&#x20;   {"description": "Оплата услуг"},

&#x20;   {"description": "Перевод на карту"},

&#x20;   {"description": "Оплата товаров"}

]



categories = \["Перевод", "Оплата"]

result = count\_operations\_by\_category(transactions, categories)

\# Вернёт {'Перевод': 2, 'Оплата': 2}

```



\## Тестирование



Для запуска тестов выполните:



```bash

pytest tests/

```



Отчет о покрытии тестами находится в файле `coverage\_report.txt` и папке `htmlcov/`.



\## Технологии



\- Python 3.9+

\- Poetry

\- Git

\- GitHub

\- pandas

\- openpyxl



\## Лицензия



MIT



\## Классы для интернет-магазина



Модуль `src/classes.py` содержит два класса:



\### `Product`

Представляет товар с атрибутами: название, описание, цена, количество.



\### `Category`

Представляет категорию товаров. Содержит атрибуты класса:

\- `category\_count` — общее количество категорий

\- `product\_count` — общее количество продуктов

