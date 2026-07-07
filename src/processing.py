"""
Модуль для обработки списков банковских операций.
"""

from typing import List, Dict, Any


def filter_by_state(operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по значению ключа 'state'.

    Args:
        operations (List[Dict[str, Any]]): Список словарей с данными операций.
        state (str): Искомое значение для ключа 'state'. По умолчанию 'EXECUTED'.

    Returns:
        List[Dict[str, Any]]: Новый список, содержащий только операции с указанным state.
    """
    return [op for op in operations if op.get('state') == state]


def sort_by_date(operations: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате (ключ 'date').

    Args:
        operations (List[Dict[str, Any]]): Список словарей с данными операций.
        descending (bool): Порядок сортировки. True — убывание (сначала новые), False — возрастание.

    Returns:
        List[Dict[str, Any]]: Новый отсортированный список.
    """
    return sorted(operations, key=lambda x: x.get('date', ''), reverse=descending)