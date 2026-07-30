import pytest
from src.widget import mask_account_card, get_date

def test_mask_account_card_card():
    account_info = "Visa Platinum 1234567890123456"
    expected = "Visa Platinum 1234 56** **** 3456"
    assert mask_account_card(account_info) == expected

def test_mask_account_card_account():
    account_info = "Счет 1234567890"
    expected = "Счет **7890"
    assert mask_account_card(account_info) == expected

def test_mask_account_card_invalid_data():
    with pytest.raises(ValueError, match="Недостаточно данных"):
        mask_account_card("invalid_data")

def test_get_date_valid():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"

def test_get_date_invalid_format():
    with pytest.raises(ValueError):
        get_date("invalid_date")