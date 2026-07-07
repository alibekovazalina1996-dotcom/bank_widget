"""
Тесты для модуля masks.
"""

import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.fixture
def valid_card_numbers():
    """Фикстура с корректными номерами карт."""
    return [
        ("1234567812345678", "1234 56** **** 5678"),
        ("1111222233334444", "1111 22** **** 4444"),
    ]


@pytest.fixture
def valid_account_numbers():
    """Фикстура с корректными номерами счетов."""
    return [
        ("12345678901234567890", "**7890"),
        ("98765432109876543210", "**3210"),
    ]


def test_get_mask_card_number_valid(valid_card_numbers):
    for card_number, expected in valid_card_numbers:
        assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_invalid():
    with pytest.raises(ValueError):
        get_mask_card_number("123456")  # слишком короткий


def test_get_mask_account_valid(valid_account_numbers):
    for account_number, expected in valid_account_numbers:
        assert get_mask_account(account_number) == expected


def test_get_mask_account_short():
    with pytest.raises(ValueError):
        get_mask_account("123")
