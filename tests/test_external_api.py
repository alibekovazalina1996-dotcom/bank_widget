import pytest
from unittest.mock import patch
import requests
from src.external_api import convert_to_rub

def test_convert_to_rub_rub():
    transaction = {"amount": "100", "currency": {"code": "RUB"}}
    assert convert_to_rub(transaction) == 100.0

@patch('src.external_api.requests.get')
def test_convert_to_rub_usd_success(mock_get):
    mock_get.return_value.json.return_value = {"result": 7500.0}
    mock_get.return_value.raise_for_status = lambda: None
    transaction = {"amount": "100", "currency": {"code": "USD"}}
    assert convert_to_rub(transaction) == 7500.0

@patch('src.external_api.requests.get')
def test_convert_to_rub_api_error(mock_get):
    mock_get.side_effect = requests.RequestException("API Error")
    transaction = {"amount": "100", "currency": {"code": "USD"}}
    assert convert_to_rub(transaction) == 100.0

def test_convert_to_rub_no_api_key(monkeypatch):
    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "")
    transaction = {"amount": "100", "currency": {"code": "USD"}}
    assert convert_to_rub(transaction) == 100.0