import pytest
import pandas as pd
from src.utils import read_excel_file, get_date_range, format_date


def test_read_excel_file():
    """Тест чтения Excel-файла."""
    df = read_excel_file('data/operations.xlsx')
    assert not df.empty
    assert 'Дата операции' in df.columns


def test_get_date_range():
    """Тест диапазона дат."""
    start, end = get_date_range('2021-12-31 23:59:59')
    assert start.month == 12
    assert start.year == 2021
    assert start.day == 1
    assert end.month == 12


def test_format_date():
    """Тест форматирования даты."""
    dt = pd.to_datetime('2021-12-31')
    assert format_date(dt) == '31.12.2021'