# Виджет банковских операций

Проект для обработки и фильтрации данных о банковских транзакциях.

---

## Описание

В проекте реализованы:

- **Модуль `processing`** – функции фильтрации и сортировки транзакций.  
- **Модуль `generators`** (новое) – генераторы для работы с большими объёмами данных.

---

## Модуль `processing` (основные функции)

### `filter_by_state(operations, state='EXECUTED')`
Фильтрует список операций по статусу.

### `sort_by_date(operations, descending=True)`
Сортирует операции по дате.

---

## Модуль `generators` (новое)

Модуль содержит три функции-генератора для обработки транзакций.

### 1. `filter_by_currency(transactions, currency_code)`
Генерирует транзакции с заданной валютой.

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))
```

### 2. `transaction_descriptions(transactions)`
Генерирует описания транзакций по очереди.

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for _ in range(3):
    print(next(descriptions))
```

### 3. `card_number_generator(start, stop)`
Генерирует номера карт в формате `XXXX XXXX XXXX XXXX`.

```python
from src.generators import card_number_generator

for card in card_number_generator(1, 5):
    print(card)
```

---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/alibekovazalina1996-dotcom/bank_widget.git
cd bank_widget
```

### 2. Установка зависимостей (опционально)

Для проверки кода и тестов установите:

```bash
pip install flake8 mypy isort pytest pytest-cov
```

Если `pip` не работает, используйте:

```bash
python -m pip install flake8 mypy isort pytest pytest-cov
```

### 3. Запуск тестов

```bash
pytest tests/test_generators.py --cov=src.generators --cov-report=html
```

После выполнения откройте файл `htmlcov/index.html` в браузере, чтобы увидеть отчёт о покрытии.

### 4. Проверка линтеров

```bash
flake8 src/ tests/
mypy src/
```

---

## Лицензия

Проект создан в учебных целях.