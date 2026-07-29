"""
Модуль с генераторами для работы с банковскими транзакциями.
"""

from typing import List, Dict, Any, Iterator, Generator


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список словарей с данными транзакций.
        currency_code: Код валюты для фильтрации (например, 'USD').

    Yields:
        Транзакция, в которой валюта соответствует заданной.
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генерирует описания транзакций по очереди.

    Args:
        transactions: Список словарей с данными транзакций.

    Yields:
        Описание очередной транзакции.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.

    Args:
        start: Начальное значение диапазона (включительно).
        stop: Конечное значение диапазона (включительно).

    Yields:
        Номер карты в формате XXXX XXXX XXXX XXXX.
    """
    for number in range(start, stop + 1):
        card_str = f"{number:016d}"
        formatted = " ".join(card_str[i:i+4] for i in range(0, 16, 4))
        yield formatted