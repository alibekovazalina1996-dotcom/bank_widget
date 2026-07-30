import pytest
from unittest.mock import patch, Mock
import requests
from src.external_api import convert_to_rub

def test_convert_to_rub_rub():
    """Тест, когда валюта уже рубли."""
    transaction = {"amount": "100", "currency": {"code": "RUB"}}
    assert convert_to_rub(transaction) == 100.0

@patch('src.external_api.requests.get')
def test_convert_to_rub_usd_success(mock_get):
    """Тест успешной конвертации USD с использованием mock."""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 7500.0}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    transaction = {"amount": "100", "currency": {"code": "USD"}}
    result = convert_to_rub(transaction)
    
    assert result == 7500.0
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100.0",
        headers={"apikey": "твой_реальный_ключ_с_сайта_apilayer.com"}
    )

@patch('src.external_api.requests.get')
def test_convert_to_rub_api_error(mock_get):
    """Тест ошибки API с использованием mock."""
    mock_get.side_effect = requests.RequestException("API Error")

    transaction = {"amount": "100", "currency": {"code": "USD"}}
    result = convert_to_rub(transaction)
    
    assert result == 100.0

@patch('src.external_api.requests.get')
def test_convert_to_rub_eur_success(mock_get):
    """Тест успешной конвертации EUR."""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 18000.0}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    transaction = {"amount": "200", "currency": {"code": "EUR"}}
    result = convert_to_rub(transaction)
    
    assert result == 18000.0
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=200.0",
        headers={"apikey": "твой_реальный_ключ_с_сайта_apilayer.com"}
    )

def test_convert_to_rub_no_api_key(monkeypatch):
    """Тест, когда нет API ключа."""
    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "")
    transaction = {"amount": "100", "currency": {"code": "USD"}}
    result = convert_to_rub(transaction)
    assert result == 100.0