import pytest
from src.processing import search_by_description, count_operations_by_category


def test_search_by_description_found():
    transactions = [
        {"description": "Перевод другу"},
        {"description": "Оплата услуг"},
        {"description": "Перевод на карту"}
    ]
    result = search_by_description(transactions, "перевод")
    assert len(result) == 2
    assert result[0]["description"] == "Перевод другу"
    assert result[1]["description"] == "Перевод на карту"


def test_search_by_description_not_found():
    transactions = [
        {"description": "Перевод другу"},
        {"description": "Оплата услуг"},
    ]
    result = search_by_description(transactions, "пополнение")
    assert result == []


def test_count_operations_by_category():
    transactions = [
        {"description": "Перевод другу"},
        {"description": "Оплата услуг"},
        {"description": "Перевод на карту"},
        {"description": "Оплата товаров"}
    ]
    categories = ["Перевод", "Оплата"]
    result = count_operations_by_category(transactions, categories)
    assert result == {"Перевод": 2, "Оплата": 2}


def test_count_operations_by_category_empty():
    assert count_operations_by_category([], ["Перевод"]) == {}
    assert count_operations_by_category([{"description": "test"}], []) == {}