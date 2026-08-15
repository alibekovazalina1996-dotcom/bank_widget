import re
from collections import Counter
from typing import List, Dict, Any


def search_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, в описании которых встречается заданная строка (без учёта регистра).

    Аргументы:
        transactions (List[Dict[str, Any]]): Список словарей с транзакциями.
        search_string (str): Строка для поиска.

    Возвращает:
        List[Dict[str, Any]]: Список транзакций, соответствующих критерию.
    """
    if not search_string:
        return transactions

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [tx for tx in transactions if pattern.search(tx.get("description", ""))]


def count_operations_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций в каждой из переданных категорий.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список словарей с транзакциями.
        categories (List[str]): Список категорий для подсчета.

    Возвращает:
        Dict[str, int]: Словарь с количеством операций по категориям.
    """
    if not transactions or not categories:
        return {}

    # Приводим категории к нижнему регистру для поиска без учёта регистра
    categories_lower = [cat.lower() for cat in categories]
    category_counter = Counter()

    for tx in transactions:
        description = tx.get("description", "").lower()
        for idx, cat in enumerate(categories_lower):
            if cat in description:
                category_counter[categories[idx]] += 1
                break  # Считаем только первое совпадение

    return dict(category_counter)