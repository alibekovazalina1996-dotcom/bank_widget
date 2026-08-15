import pytest
import json
from src.services import cashback_analysis, investment_bank, simple_search, phone_search, transfer_search
from src.utils import read_excel_file


@pytest.fixture
def df():
    """Фикстура с данными."""
    return read_excel_file('data/operations.xlsx')


def test_cashback_analysis(df):
    """Тест анализа кешбэка."""
    result = cashback_analysis(df, 2021, 12)
    data = json.loads(result)
    assert isinstance(data, dict)
    assert "Переводы" in data


def test_investment_bank(df):
    """Тест инвесткопилки."""
    result = investment_bank(df, "2021-12", 50)
    assert isinstance(result, float)
    assert result > 0


def test_simple_search(df):
    """Тест поиска по подстроке."""
    result = simple_search(df, "Газпром")
    data = json.loads(result)
    assert isinstance(data, list)
    assert len(data) > 0


def test_phone_search(df):
    """Тест поиска телефонов."""
    result = phone_search(df)
    data = json.loads(result)
    assert isinstance(data, list)
    assert len(data) > 0


def test_transfer_search(df):
    """Тест поиска переводов."""
    result = transfer_search(df)
    data = json.loads(result)
    assert isinstance(data, list)
    assert len(data) > 0