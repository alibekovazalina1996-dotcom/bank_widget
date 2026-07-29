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
  
## Тестирование  
  
Для запуска тестов выполните:  
  
```bash  
pytest tests/  
```  
  
Отчет о покрытии тестами находится в файле `coverage_report.txt`.  
  
## Технологии  
  
- Python 3.9+  
- Poetry  
- Git  
- GitHub  
  
## Лицензия  
  
MIT  
