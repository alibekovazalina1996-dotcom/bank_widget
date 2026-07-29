# Bank Widget Project  
  
## Генераторы для работы с транзакциями  
  
Модуль `generators.py` содержит три функции-генератора:  
  
### 1. `filter_by_currency(transactions, currency)`  
Фильтрует транзакции по заданной валюте.  
Пример:  
`for tx in filter_by_currency(transactions, "USD"): print(tx)`  
  
### 2. `transaction_descriptions(transactions)`  
Генерирует описания транзакций по очереди.  
Пример:  
`for desc in transaction_descriptions(transactions): print(desc)`  
  
### 3. `card_number_generator(start, stop)`  
Генерирует номера карт в формате XXXX XXXX XXXX XXXX.  
Пример:  
`for card in card_number_generator(1, 5): print(card)`  
  
## Покрытие тестами  
Отчет о покрытии тестами находится в файле `coverage_report.txt`.  
