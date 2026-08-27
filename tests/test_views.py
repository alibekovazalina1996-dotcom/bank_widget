import pytest
import json
from src.views import get_greeting, main_page, events_page


def test_get_greeting():
    """Тест приветствия."""
    greeting = get_greeting()
    assert greeting in ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]


def test_main_page():
    """Тест главной страницы."""
    result = main_page("2021-12-31 23:59:59")
    data = json.loads(result)
    assert "greeting" in data
    assert "cards" in data
    assert "top_transactions" in data
    assert "currency_rates" in data
    assert "stock_prices" in data


def test_events_page():
    """Тест страницы событий."""
    result = events_page("2021-12-31 23:59:59", "M")
    data = json.loads(result)
    assert "expenses" in data
    assert "income" in data
    assert "total_amount" in data["expenses"]
    assert "currency_rates" in data
    assert "stock_prices" in data