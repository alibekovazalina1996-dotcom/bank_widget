"""
Тесты для модуля processing.
"""

import pytest
from src.processing import filter_by_state, sort_by_date  # ВАЖНО: правильный импорт


@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2024-02-20T12:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-01T14:00:00"},
        {"id": 4, "state": "CANCELED", "date": "2024-04-10T09:00:00"},
    ]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2, 4]),
        ("PENDING", []),
    ],
)
def test_filter_by_state(sample_data, state, expected_ids):
    filtered = filter_by_state(sample_data, state)
    assert [item["id"] for item in filtered] == expected_ids


@pytest.mark.parametrize(
    "descending, expected_order",
    [
        (True, [4, 3, 2, 1]),  # убывание
        (False, [1, 2, 3, 4]),  # возрастание
    ],
)
def test_sort_by_date(sample_data, descending, expected_order):
    sorted_data = sort_by_date(sample_data, descending)
    assert [item["id"] for item in sorted_data] == expected_order