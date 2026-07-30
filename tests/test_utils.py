import pytest
import json
from src.utils import load_transactions


def test_load_transactions_success(tmp_path):
    """Тест успешной загрузки файла."""
    data = [{"id": 1, "amount": 100}]
    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = load_transactions(str(file_path))
    assert result == data


def test_load_transactions_not_found():
    """Тест для несуществующего файла."""
    assert load_transactions("non_existent.json") == []


def test_load_transactions_empty_file(tmp_path):
    """Тест для пустого файла."""
    file_path = tmp_path / "empty.json"
    file_path.write_text("", encoding="utf-8")

    assert load_transactions(str(file_path)) == []


def test_load_transactions_not_list(tmp_path):
    """Тест, когда файл содержит не список."""
    file_path = tmp_path / "not_list.json"
    file_path.write_text('{"key": "value"}', encoding="utf-8")

    assert load_transactions(str(file_path)) == []