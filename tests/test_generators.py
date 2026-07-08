"""
Тесты для модуля generators.
"""

import pytest

from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)


@pytest.fixture
def test_transactions():
    """Возвращает список транзакций для тестирования."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
        },
    ]


def test_filter_by_currency_usd(test_transactions):
    """Тест фильтрации по валюте USD."""
    usd_transactions = list(filter_by_currency(test_transactions, "USD"))
    assert len(usd_transactions) == 2
    for t in usd_transactions:
        assert t["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_rub(test_transactions):
    """Тест фильтрации по валюте RUB."""
    rub_transactions = list(filter_by_currency(test_transactions, "RUB"))
    assert len(rub_transactions) == 1
    assert rub_transactions[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_currency_no_match(test_transactions):
    """Тест фильтрации по валюте, которой нет в данных."""
    eur_transactions = list(filter_by_currency(test_transactions, "EUR"))
    assert len(eur_transactions) == 0


def test_filter_by_currency_empty_list():
    """Тест фильтрации с пустым списком."""
    result = list(filter_by_currency([], "USD"))
    assert result == []


@pytest.mark.parametrize(
    "currency, expected_count",
    [
        ("USD", 2),
        ("RUB", 1),
        ("EUR", 0),
    ],
)
def test_filter_by_currency_parametrized(test_transactions, currency, expected_count):
    """Параметризованный тест фильтрации по валюте."""
    result = list(filter_by_currency(test_transactions, currency))
    assert len(result) == expected_count


def test_transaction_descriptions(test_transactions):
    """Тест получения описаний транзакций."""
    descriptions = list(transaction_descriptions(test_transactions))
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
    ]
    assert descriptions == expected


def test_transaction_descriptions_empty_list():
    """Тест с пустым списком транзакций."""
    descriptions = list(transaction_descriptions([]))
    assert descriptions == []


def test_transaction_descriptions_missing_description():
    """Тест с транзакцией, у которой отсутствует ключ 'description'."""
    transactions = [{"id": 1}, {"id": 2, "description": "test"}]
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["", "test"]


def test_card_number_generator_start_stop():
    """Тест генерации номеров карт в диапазоне."""
    cards = list(card_number_generator(1, 5))
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    assert cards == expected


def test_card_number_generator_single():
    """Тест генерации одного номера."""
    cards = list(card_number_generator(9999, 9999))
    assert cards == ["0000 0000 0000 9999"]


def test_card_number_generator_large_number():
    """Тест генерации с большим числом."""
    cards = list(card_number_generator(9999999999999999, 9999999999999999))
    assert cards == ["9999 9999 9999 9999"]


@pytest.mark.parametrize(
    "start, stop, expected_first, expected_last",
    [
        (1, 3, "0000 0000 0000 0001", "0000 0000 0000 0003"),
        (9990, 9992, "0000 0000 0000 9990", "0000 0000 0000 9992"),
    ],
)
def test_card_number_generator_parametrized(
    start,
    stop,
    expected_first,
    expected_last
):
    """Параметризованный тест генератора номеров карт."""
    cards = list(card_number_generator(start, stop))
    assert cards[0] == expected_first
    assert cards[-1] == expected_last
