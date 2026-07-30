import pytest
from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number_valid():
    """Тест для корректного номера карты."""
    card_number = "1234567890123456"
    assert get_mask_card_number(card_number) == "1234 56** **** 3456"


def test_get_mask_card_number_invalid_length():
    """Тест для некорректной длины номера карты."""
    with pytest.raises(ValueError, match="должен содержать ровно 16 цифр"):
        get_mask_card_number("1234")


def test_get_mask_account_valid():
    """Тест для корректного номера счёта."""
    account_number = "1234567890"
    assert get_mask_account(account_number) == "**7890"


def test_get_mask_account_valid_min_length():
    """Тест для счёта из 4 цифр."""
    assert get_mask_account("1234") == "**1234"


def test_get_mask_account_invalid_length():
    """Тест для слишком короткого номера счёта."""
    with pytest.raises(ValueError, match="минимум 4 цифры"):
        get_mask_account("123")