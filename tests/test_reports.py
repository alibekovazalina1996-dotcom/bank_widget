import pytest
import json
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.utils import read_excel_file


@pytest.fixture
def df():
    """Фикстура с данными."""
    return read_excel_file('data/operations.xlsx')


def test_spending_by_category(df):
    """Тест трат по категории."""
    result = spending_by_category(df, "Супермаркеты", "2021-12-31")
    data = json.loads(result)
    assert data["category"] == "Супермаркеты"
    assert "total_spent" in data


def test_spending_by_weekday(df):
    """Тест трат по дням недели."""
    result = spending_by_weekday(df, "2021-12-31")
    data = json.loads(result)
    assert "Понедельник" in data
    assert isinstance(data["Понедельник"], float)


def test_spending_by_workday(df):
    """Тест трат по рабочим дням."""
    result = spending_by_workday(df, "2021-12-31")
    data = json.loads(result)
    assert "workday" in data
    assert "weekend" in data